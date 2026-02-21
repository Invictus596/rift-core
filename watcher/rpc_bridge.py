"""
RPC Bridge Module - Connects Python Watcher to Starknet Verifier Contract

This module provides the bridge between the Bitcoin mempool watcher
and the Starknet Verifier contract using starknet.py for RPC communication.
"""

import os
from typing import Optional, Dict, Any
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.serialization import serializer_for_function
from starknet_py.abi.v2 import AbiParser

# Configuration
KATANA_RPC_URL = os.getenv("KATANA_RPC_URL", "http://localhost:5050")
VERIFIER_CONTRACT_ADDRESS = os.getenv("VERIFIER_CONTRACT_ADDRESS", "0x0")

# Katana default account credentials (from katana-account.json)
# These are the default Katana accounts - update if using custom setup
KATANA_ACCOUNT_ADDRESS = os.getenv("KATANA_ACCOUNT_ADDRESS", "0x127fd5f2f9c6f5a0d6f5e5c5b5a5f5e5d5c5b5a5f5e5d5c5b5a5f5e5d5c5b5a5")
KATANA_PRIVATE_KEY = os.getenv("KATANA_PRIVATE_KEY", "0x71d7bb07b9a64f6f78ac4c816aff4da9")


class RpcBridge:
    """
    Bridge class for communicating with the Starknet Verifier contract.
    
    Handles:
    - Connection to Katana/Starknet node
    - Account setup and signing
    - Contract interaction (declare, deploy, invoke)
    - Transaction status monitoring
    """
    
    def __init__(self, rpc_url: str = KATANA_RPC_URL):
        self.rpc_url = rpc_url
        self.client = FullNodeClient(node_url=rpc_url)
        self.account: Optional[Account] = None
        self.verifier_contract: Optional[Contract] = None
        self.verifier_address: Optional[str] = None
        
    async def setup_account(
        self, 
        address: str = KATANA_ACCOUNT_ADDRESS,
        private_key: str = KATANA_PRIVATE_KEY
    ) -> None:
        """
        Initialize the Starknet account for transaction signing.
        
        Args:
            address: Account address (hex string)
            private_key: Private key for signing (hex string)
        """
        # Ensure proper hex format
        if not address.startswith("0x"):
            address = f"0x{address}"
        if not private_key.startswith("0x"):
            private_key = f"0x{private_key}"
            
        self.account = Account(
            client=self.client,
            address=address,
            key_pair=KeyPair.from_private_key(int(private_key, 16)),
            chain=await self.client.get_chain_id()
        )
        print(f"[*] Account initialized: {address[:10]}...")
        
    async def load_verifier_contract(self, contract_address: str) -> None:
        """
        Load an existing Verifier contract instance.
        
        Args:
            contract_address: Deployed contract address (hex string)
        """
        if not contract_address.startswith("0x"):
            contract_address = f"0x{contract_address}"
            
        # Load the contract using the compiled ABI
        self.verifier_contract = await Contract.from_address(
            address=contract_address,
            provider=self.account
        )
        self.verifier_address = contract_address
        print(f"[*] Verifier contract loaded: {contract_address}")
        
    async def declare_and_deploy_verifier(
        self, 
        contract_path: str = None
    ) -> Dict[str, Any]:
        """
        Declare and deploy the Verifier contract (for initial setup).
        
        Args:
            contract_path: Path to the compiled contract JSON
            
        Returns:
            Dict with contract_address, declare_hash, deploy_hash
        """
        if contract_path is None:
            # Try both possible paths for the compiled contract
            contract_paths = [
                "/home/invictus/rift-core-internal/contracts/target/dev/rift_core_internal_Verifier.contract_class.json",
                "/home/invictus/rift-core-internal/contracts/target/dev/rift_verifier_Verifier.contract_class.json"
            ]
            for path in contract_paths:
                if os.path.exists(path):
                    contract_path = path
                    break
                    
        if contract_path is None or not os.path.exists(contract_path):
            raise FileNotFoundError(
                "Compiled contract not found. Please run 'scarb build' first. "
                "Tried: rift_core_internal_Verifier.contract_class.json, "
                "rift_verifier_Verifier.contract_class.json"
            )
        
        # Read the compiled contract
        with open(contract_path, "r") as f:
            contract_compiled = f.read()
            
        import json
        import subprocess
        
        contract_dict = json.loads(contract_compiled)
        
        # Extract ABI from the contract  
        abi = contract_dict.get("abi", [])
        
        # Compute class hash using starkli CLI
        try:
            result = subprocess.run(
                ["starkli", "class-hash", contract_path],
                capture_output=True,
                text=True,
                check=True
            )
            class_hash = int(result.stdout.strip(), 16)
            print(f"[*] Computed class hash: {hex(class_hash)}")
        except Exception as e:
            print(f"[!] Could not compute class hash with starkli: {e}")
            raise RuntimeError(
                "Failed to compute class hash. Please ensure starkli is installed and in PATH. "
                "Alternatively, compute it manually and pass it as a parameter."
            )
            
        # Declare the contract first
        declare_result = await self.account.sign_declare_v2(
            compiled_contract=contract_compiled,
            compiled_class_hash=class_hash
        )
        
        # Send the declare transaction
        declare_tx = await self.account.client.send_transaction(declare_result)
        await self.account.client.wait_for_tx(declare_tx)
        print(f"[*] Contract declared: {hex(class_hash)}")
        
        # Now deploy using the class hash
        from starknet_py.contract import Contract
        deploy_result = await Contract.deploy_contract_v1(
            account=self.account,
            class_hash=class_hash,
            abi=abi,
            constructor_args={"owner": self.account.address},
            max_fee=int(1e16)  # 0.01 ETH for deployment
        )
        await deploy_result.wait_for_acceptance()
        print(f"[*] Contract deployed: {hex(deploy_result.deployed_contract_address)}")

        # Load the contract instance
        self.verifier_contract = deploy_result.deployed_contract
        self.verifier_address = hex(deploy_result.deployed_contract_address)

        return {
            "contract_address": self.verifier_address,
            "declare_hash": hex(declare_tx),
            "deploy_hash": hex(deploy_result.hash)
        }
        
    async def verify_signature(
        self,
        tx_hash: int,
        public_key_x: int,
        public_key_y: int,
        msg_hash: int,
        r: int,
        s: int
    ) -> Dict[str, Any]:
        """
        Call the verify_secp256k1_signature function on the Verifier contract.
        
        Args:
            tx_hash: Transaction hash (felt252)
            public_key_x: X coordinate of public key (u256)
            public_key_y: Y coordinate of public key (u256)
            msg_hash: Message hash (u256)
            r: Signature R component (u256)
            s: Signature S component (u256)
            
        Returns:
            Dict with invocation result and transaction info
        """
        if self.verifier_contract is None:
            raise RuntimeError("Verifier contract not loaded. Call load_verifier_contract first.")
            
        # Prepare u256 values as (low, high) tuples for Cairo
        # u256 in Cairo is represented as two u128 values
        def to_u256(value: int) -> tuple:
            low = value & ((1 << 128) - 1)
            high = (value >> 128) & ((1 << 128) - 1)
            return (low, high)
            
        # Convert tx_hash to felt (ensure it's within felt range)
        felt_tx_hash = tx_hash % (2 ** 251)
        
        # Prepare the function call
        invocation = await self.verifier_contract.functions["verify_secp256k1_signature"].invoke(
            tx_hash=felt_tx_hash,
            public_key_x=to_u256(public_key_x),
            public_key_y=to_u256(public_key_y),
            msg_hash=to_u256(msg_hash),
            r=to_u256(r),
            s=to_u256(s),
            max_fee=int(1e15)  # 0.001 ETH
        )
        
        # Wait for the transaction to be accepted
        result = await invocation.wait_for_acceptance()
        
        # Get the verification count after the call
        verification_count = await self.verifier_contract.functions["get_verification_count"].call()
        
        return {
            "success": True,
            "tx_hash": hex(result.hash),
            "verification_count": verification_count,
            "contract_address": self.verifier_address
        }
        
    async def is_verified(self, tx_hash: int) -> bool:
        """
        Check if a transaction has been verified.
        
        Args:
            tx_hash: Transaction hash to check
            
        Returns:
            True if verified, False otherwise
        """
        if self.verifier_contract is None:
            raise RuntimeError("Verifier contract not loaded.")
            
        felt_tx_hash = tx_hash % (2 ** 251)
        result = await self.verifier_contract.functions["is_verified"].call(tx_hash=felt_tx_hash)
        return result
        
    async def get_verification_count(self) -> int:
        """
        Get the total number of verified transactions.
        
        Returns:
            Total verification count
        """
        if self.verifier_contract is None:
            raise RuntimeError("Verifier contract not loaded.")
            
        result = await self.verifier_contract.functions["get_verification_count"].call()
        return result
        
    async def get_owner(self) -> str:
        """
        Get the contract owner address.
        
        Returns:
            Owner address (hex string)
        """
        if self.verifier_contract is None:
            raise RuntimeError("Verifier contract not loaded.")
            
        result = await self.verifier_contract.functions["get_owner"].call()
        return hex(result)


async def test_bridge():
    """Test function for the RPC bridge."""
    print("[*] Testing RPC Bridge...")
    
    bridge = RpcBridge()
    
    try:
        # Initialize account
        await bridge.setup_account()
        
        # Try to load a deployed contract (if address is known)
        # For testing, this will likely fail until contract is deployed
        if VERIFIER_CONTRACT_ADDRESS != "0x0":
            await bridge.load_verifier_contract(VERIFIER_CONTRACT_ADDRESS)
            
            # Test a mock verification
            mock_tx_hash = 0x1234567890abcdef
            mock_pubkey_x = 0xabcdef1234567890
            mock_pubkey_y = 0x9876543210fedcba
            mock_msg_hash = 0xfedcba0987654321
            mock_r = 0x1111111111111111
            mock_s = 0x2222222222222222
            
            result = await bridge.verify_signature(
                tx_hash=mock_tx_hash,
                public_key_x=mock_pubkey_x,
                public_key_y=mock_pubkey_y,
                msg_hash=mock_msg_hash,
                r=mock_r,
                s=mock_s
            )
            print(f"[*] Mock verification result: {result}")
        else:
            print("[*] No verifier contract address set. Skipping verification test.")
            
    except Exception as e:
        print(f"[!] Test failed: {e}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_bridge())
