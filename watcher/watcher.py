import time
import random
import binascii
import asyncio
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configuration
MOCK_MODE = True  # Set to True for testing without a real Bitcoin node
BITCOIN_RPC_URL = "http://user:password@localhost:18332"  # Replace with your RPC credentials
POLL_INTERVAL = 2  # Poll every 2 seconds
RIFT_HEX_TAG = "52494654"  # Hex representation of "RIFT"

# Starknet RPC Configuration
STARKNET_RPC_MODE = False  # Set to True to enable Starknet contract interaction
KATANA_RPC_URL = "http://localhost:5050"
VERIFIER_CONTRACT_ADDRESS = "0x0"  # Set after deployment

def connect_to_bitcoin_node():
    """Connect to the Bitcoin Testnet RPC node"""
    try:
        rpc_connection = AuthServiceProxy(BITCOIN_RPC_URL)
        # Test the connection
        rpc_connection.getblockchaininfo()
        print("[*] Successfully connected to Bitcoin Testnet node")
        return rpc_connection
    except Exception as e:
        print(f"[!] Failed to connect to Bitcoin node: {e}")
        return None

def generate_mock_transaction():
    """Generate a mock transaction for testing purposes"""
    # Generate a random transaction ID
    tx_id = ''.join(random.choices('0123456789abcdef', k=64))
    
    # Randomly decide if this transaction contains the RIFT tag
    has_rift_tag = random.choice([True, False])
    
    if has_rift_tag:
        # Create a mock transaction with the RIFT tag in OP_RETURN
        # Format: random prefix + RIFT hex tag + random suffix
        op_return_data = ''.join(random.choices('0123456789abcdef', k=20)) + RIFT_HEX_TAG + ''.join(random.choices('0123456789abcdef', k=20))
        slen = hex(len(op_return_data)//2)[2:]
        raw_tx = f"0200000001{'a'*64}000000001976a914{'b'*40}88acffffffff010000000000000000{slen}6a{slen}{op_return_data}00000000"
    else:
        # Create a mock transaction without the RIFT tag
        op_return_data = ''.join(random.choices('0123456789abcdef', k=40))
        slen = hex(len(op_return_data)//2)[2:]
        raw_tx = f"0200000001{'c'*64}000000001976a914{'d'*40}88acffffffff010000000000000000{slen}6a{slen}{op_return_data}00000000"
    
    return {
        'txid': tx_id,
        'hex': raw_tx
    }

def get_raw_mempool_transactions(rpc_connection):
    """Get all raw transactions from the mempool"""
    if MOCK_MODE:
        # In mock mode, generate random transactions
        num_transactions = random.randint(0, 5)  # Randomly generate 0-5 transactions
        transactions = []
        
        for _ in range(num_transactions):
            mock_tx = generate_mock_transaction()
            transactions.append(mock_tx)
        
        return transactions
    else:
        # In real mode, get actual transactions from the Bitcoin node
        try:
            txids = rpc_connection.getrawmempool()
            transactions = []
            
            for txid in txids:
                raw_tx = rpc_connection.getrawtransaction(txid)
                transactions.append({
                    'txid': txid,
                    'hex': raw_tx
                })
            
            return transactions
        except Exception as e:
            print(f"[!] Error getting mempool transactions: {e}")
            return []

def contains_rift_tag(transaction_hex):
    """Check if a transaction contains the RIFT tag in OP_RETURN"""
    # Look for the hex tag "52494654" which represents "RIFT"
    return RIFT_HEX_TAG.lower() in transaction_hex.lower()

def extract_op_return_data(transaction_hex):
    """Extract OP_RETURN data from a transaction hex"""
    # Bitcoin OP_RETURN format: 6a <push_bytes> <data>
    # Where 6a is OP_RETURN opcode, followed by pushdata length, then the data
    # 
    # Note: '6a' can appear in P2PKH scripts (76a914 = OP_DUP OP_HASH160 PUSHDATA(20))
    # We need to find the OP_RETURN in an output script, which comes after:
    # - Output value (8 bytes little-endian)
    # - Script length varint
    # - Then: 6a (OP_RETURN) <push> <data>
    try:
        # Look for the pattern: 6a followed by a pushdata byte, then data
        # We search for all '6a' and validate the context
        import re
        for match in re.finditer(r'6a([0-9a-f]{2})', transaction_hex.lower()):
            pos = match.start()
            push_len = int(match.group(1), 16)
            
            # Sanity check: OP_RETURN data should be reasonable (1-80 bytes)
            if 0 < push_len <= 80:
                data_start = pos + 4  # Skip '6a' + length byte (2 hex chars each)
                data_end = data_start + (push_len * 2)
                if data_end <= len(transaction_hex):
                    op_return_data = transaction_hex[data_start:data_end]
                    return op_return_data
    except Exception:
        pass

    return ""


async def send_to_verifier(tx_hash: str, tx_hex: str):
    """
    Send detected transaction to the Starknet Verifier contract.
    
    Args:
        tx_hash: Bitcoin transaction ID (hex string)
        tx_hex: Full transaction hex data
    """
    if not STARKNET_RPC_MODE:
        print(f"    [*] STARKNET_RPC_MODE disabled - skipping contract call")
        return
        
    try:
        from rpc_bridge import RpcBridge
        from serializer import hex_to_felt_array
        
        # Initialize the bridge
        bridge = RpcBridge(rpc_url=KATANA_RPC_URL)
        
        # Setup account (using environment variables or defaults)
        await bridge.setup_account()
        
        # Load the verifier contract
        if VERIFIER_CONTRACT_ADDRESS == "0x0":
            print(f"    [!] Verifier contract address not set")
            return
            
        await bridge.load_verifier_contract(VERIFIER_CONTRACT_ADDRESS)
        
        # Convert transaction hash to felt
        tx_hash_felt = int(tx_hash, 16) if not tx_hash.startswith('0x') else int(tx_hash, 16)
        
        # Convert transaction hex to felt array for the contract
        tx_data_felts = hex_to_felt_array(tx_hex)
        
        # For mock testing, we'll use placeholder signature values
        # In production, these would be extracted from the Bitcoin transaction
        mock_public_key_x = 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
        mock_public_key_y = 0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321
        mock_msg_hash = sum(tx_data_felts) % (2 ** 256)  # Simple hash of tx data
        mock_r = 0x1111111111111111111111111111111111111111111111111111111111111111
        mock_s = 0x2222222222222222222222222222222222222222222222222222222222222222
        
        print(f"    [*] Calling verify_secp256k1_signature on Verifier contract...")
        
        # Call the verifier contract
        result = await bridge.verify_signature(
            tx_hash=tx_hash_felt,
            public_key_x=mock_public_key_x,
            public_key_y=mock_public_key_y,
            msg_hash=mock_msg_hash,
            r=mock_r,
            s=mock_s
        )
        
        print(f"    [+] Verification successful!")
        print(f"        Starknet Tx Hash: {result['tx_hash']}")
        print(f"        Total Verifications: {result['verification_count']}")
        
    except Exception as e:
        print(f"    [!] Error calling verifier contract: {e}")

def main():
    print(f"[*] Starting Rift Watcher (MOCK_MODE: {MOCK_MODE})")
    print(f"[*] Looking for transactions with OP_RETURN containing hex tag: {RIFT_HEX_TAG} ('RIFT')")
    print(f"[*] Starknet RPC Mode: {STARKNET_RPC_MODE}")
    if STARKNET_RPC_MODE:
        print(f"    Katana RPC: {KATANA_RPC_URL}")
        print(f"    Verifier Contract: {VERIFIER_CONTRACT_ADDRESS}")
    print("-" * 50)

    rpc_connection = None
    if not MOCK_MODE:
        rpc_connection = connect_to_bitcoin_node()
        if not rpc_connection:
            print("[!] Cannot proceed without Bitcoin node connection. Exiting...")
            return

    print("[*] Starting mempool monitoring...")
    print("-" * 50)

    try:
        iteration_count = 0
        while True:
            transactions = get_raw_mempool_transactions(rpc_connection)

            for tx in transactions:
                tx_hex = tx['hex']

                if contains_rift_tag(tx_hex):
                    # Extract OP_RETURN data to show what was found
                    op_return_data = extract_op_return_data(tx_hex)

                    print(f"[+] RIFT PROTOCOL TX DETECTED")
                    print(f"    Transaction ID: {tx['txid']}")
                    print(f"    Raw Hex Data: {tx_hex}")
                    print(f"    OP_RETURN Data: {op_return_data}")
                    
                    # Send to Starknet Verifier contract
                    asyncio.run(send_to_verifier(tx['txid'], tx_hex))
                    
                    print("-" * 50)

            iteration_count += 1
            if MOCK_MODE and iteration_count >= 20:  # Limit iterations in mock mode for testing
                print(f"[*] Completed {iteration_count} polling cycles in mock mode. Exiting...")
                break

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print(f"\n[*] Stopping Rift Watcher after {iteration_count} polling cycles...")
        exit(0)

if __name__ == "__main__":
    main()