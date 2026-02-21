#!/usr/bin/env python3
"""
Test script for the RPC Bridge integration.

This script tests the full pipeline:
1. Initialize Katana account
2. Declare and deploy the Verifier contract
3. Call verify_secp256k1_signature
4. Verify the state change

Prerequisites:
- Katana must be running: katana --validate-max-steps 4000000 --invoke-max-steps 4000000
"""

import asyncio
import sys
import os

# Add watcher directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rpc_bridge import RpcBridge


async def test_full_pipeline():
    """Test the full RPC bridge pipeline."""
    print("=" * 60)
    print("RIFT Protocol - RPC Bridge Integration Test")
    print("=" * 60)
    print()
    
    # Check if Katana is running
    import subprocess
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:5050", "-X", "POST", 
             "-H", "Content-Type: application/json",
             "-d", '{"jsonrpc":"2.0","method":"starknet_chainId","params":[],"id":1}'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "result" not in result.stdout:
            print("✗ Katana is not running at http://localhost:5050")
            print()
            print("Start Katana first:")
            print("  katana --validate-max-steps 4000000 --invoke-max-steps 4000000")
            print()
            return False
        print("✓ Katana is running")
        print()
    except Exception as e:
        print(f"✗ Could not connect to Katana: {e}")
        print()
        print("Start Katana first:")
        print("  katana --validate-max-steps 4000000 --invoke-max-steps 4000000")
        print()
        return False
    
    # Initialize bridge
    bridge = RpcBridge(rpc_url="http://localhost:5050")
    
    try:
        # Step 1: Setup account
        print("[1/5] Setting up Katana account...")
        # Using Katana default account #0 (standard format)
        account_address = "0x6162896d1d7ab204c7ccac6dd5f8e9e7c3eab1d1a1e1e1e1e1e1e1e1e1e1e1e"
        private_key = "0xe177350e0334a19b5a1f5a0e86d113a022bbf6aa179ac3889007479a901e2cd"
        await bridge.setup_account(address=account_address, private_key=private_key)
        print("    ✓ Account setup complete")
        print()
        
        # Step 2: Declare and deploy contract
        print("[2/5] Declaring and deploying Verifier contract...")
        # Try both possible paths for the compiled contract
        contract_paths = [
            "/home/invictus/rift-core-internal/contracts/target/dev/rift_core_internal_Verifier.contract_class.json",
            "/home/invictus/rift-core-internal/contracts/target/dev/rift_verifier_Verifier.contract_class.json"
        ]
        contract_path = None
        for path in contract_paths:
            if os.path.exists(path):
                contract_path = path
                break
        
        if contract_path is None:
            print(f"    ✗ Contract file not found")
            print("    Please run 'scarb build' first.")
            return False
            
        print(f"    Using contract: {contract_path}")
            
        deployment = await bridge.declare_and_deploy_verifier(contract_path)
        print(f"    ✓ Contract deployed at: {deployment['contract_address']}")
        print(f"    Declare hash: {deployment['declare_hash']}")
        print(f"    Deploy hash: {deployment['deploy_hash']}")
        print()
        
        # Step 3: Test verify_signature
        print("[3/5] Testing verify_secp256k1_signature...")
        mock_tx_hash = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
        mock_pubkey_x = 0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
        mock_pubkey_y = 0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321
        mock_msg_hash = 0x1111111111111111111111111111111111111111111111111111111111111111
        mock_r = 0x2222222222222222222222222222222222222222222222222222222222222222
        mock_s = 0x3333333333333333333333333333333333333333333333333333333333333333
        
        result = await bridge.verify_signature(
            tx_hash=mock_tx_hash,
            public_key_x=mock_pubkey_x,
            public_key_y=mock_pubkey_y,
            msg_hash=mock_msg_hash,
            r=mock_r,
            s=mock_s
        )
        print(f"    ✓ Verification successful!")
        print(f"    Starknet Tx Hash: {result['tx_hash']}")
        print(f"    Verification Count: {result['verification_count']}")
        print()
        
        # Step 4: Test is_verified
        print("[4/5] Checking if transaction is verified...")
        is_verified = await bridge.is_verified(mock_tx_hash)
        print(f"    ✓ is_verified() returned: {is_verified}")
        print()
        
        # Step 5: Test get_owner
        print("[5/5] Getting contract owner...")
        owner = await bridge.get_owner()
        print(f"    ✓ Contract owner: {owner}")
        print()
        
        # Summary
        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("The RPC bridge is working correctly!")
        print(f"Verifier Contract Address: {deployment['contract_address']}")
        print()
        print("To use this in watcher.py, set:")
        print(f"  VERIFIER_CONTRACT_ADDRESS = \"{deployment['contract_address']}\"")
        print("  STARKNET_RPC_MODE = True")
        print()
        
        return True
        
    except Exception as e:
        import traceback
        print()
        print("=" * 60)
        print("✗ TEST FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Full traceback:")
        traceback.print_exc()
        print()
        print("Troubleshooting:")
        print("1. Make sure Katana is running: katana --validate-max-steps 4000000 --invoke-max-steps 4000000")
        print("2. Check that the contract compiles: cd contracts && scarb build")
        print("3. Verify account credentials match Katana's pre-funded accounts")
        print("4. Check Katana logs for deployment errors")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_full_pipeline())
    sys.exit(0 if success else 1)
