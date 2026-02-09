import time
import random
import binascii
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configuration
MOCK_MODE = True  # Set to True for testing without a real Bitcoin node
BITCOIN_RPC_URL = "http://user:password@localhost:18332"  # Replace with your RPC credentials
POLL_INTERVAL = 2  # Poll every 2 seconds
RIFT_HEX_TAG = "52494654"  # Hex representation of "RIFT"

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
    # This is a simplified extraction - in reality, parsing Bitcoin transactions
    # requires more sophisticated handling of the transaction format
    try:
        # Find the OP_RETURN opcode (0x6a) followed by the data
        op_return_pos = transaction_hex.find('6a')
        if op_return_pos != -1:
            # Extract the next few bytes as potential OP_RETURN data
            start = op_return_pos + 2  # Skip the 6a opcode
            # Get the length byte and corresponding data
            if start + 2 <= len(transaction_hex):
                length_hex = transaction_hex[start:start+2]
                try:
                    length = int(length_hex, 16)
                    data_start = start + 2
                    data_end = data_start + (length * 2)  # Each byte is represented by 2 hex chars
                    if data_end <= len(transaction_hex):
                        op_return_data = transaction_hex[data_start:data_end]
                        return op_return_data
                except ValueError:
                    pass
    except Exception:
        pass
    
    return ""

def main():
    print(f"[*] Starting Rift Watcher (MOCK_MODE: {MOCK_MODE})")
    print(f"[*] Looking for transactions with OP_RETURN containing hex tag: {RIFT_HEX_TAG} ('RIFT')")
    
    rpc_connection = None
    if not MOCK_MODE:
        rpc_connection = connect_to_bitcoin_node()
        if not rpc_connection:
            print("[!] Cannot proceed without Bitcoin node connection. Exiting...")
            return
    
    print("[*] Starting mempool monitoring...")
    
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