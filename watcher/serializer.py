import math


def hex_to_felt_array(hex_string):
    """
    Convert a hex string to an array of field elements (felts) for Starknet.
    
    Args:
        hex_string (str): A raw hex string (without '0x' prefix)
        
    Returns:
        list: A list of decimal integers (felts) ready for Cairo
    """
    # Remove '0x' prefix if present
    if hex_string.startswith('0x') or hex_string.startswith('0X'):
        hex_string = hex_string[2:]
    
    # Calculate the number of 31-byte chunks needed
    # Each byte is represented by 2 hex characters
    total_bytes = len(hex_string) // 2
    
    # Calculate number of chunks (ceiling division)
    num_chunks = math.ceil(total_bytes / 31)
    
    felts = []
    
    for i in range(num_chunks):
        # Calculate start and end positions for this chunk
        start_idx = i * 31 * 2  # Each byte is 2 hex chars
        end_idx = min((i + 1) * 31 * 2, len(hex_string))
        
        # Extract the hex chunk
        chunk_hex = hex_string[start_idx:end_idx]
        
        # Pad the chunk if it's smaller than 31 bytes (62 hex chars)
        if len(chunk_hex) < 62:
            # Pad with zeros at the end (right-padding)
            chunk_hex = chunk_hex.ljust(62, '0')
        
        # Convert hex to integer (felt)
        felt = int(chunk_hex, 16)
        felts.append(felt)
    
    return felts


def main():
    """Test the hex_to_felt_array function with mock data"""
    print("Testing hex_to_felt_array function:")
    print("=" * 50)

    # Create a sample hex string similar to what would come from Bitcoin transactions
    # This simulates a typical Bitcoin transaction hex (valid hex chars only: 0-9, a-f)
    sample_tx_hex = "0200000001abcd1234ef567890abcd1234ef567890abcd1234ef567890abcd1234ef567890000000001976a914efab5678cdab1234efab5678cdab1234efab567888acffffffff0100000000000000001976a914abab3456cdab7890abab3456cdab7890abab345688ac00000000"

    print(f"Sample transaction hex: {sample_tx_hex[:64]}...")  # Show first 64 chars
    print(f"Full length: {len(sample_tx_hex)} characters")
    print()

    # Convert to felt array
    felt_array = hex_to_felt_array(sample_tx_hex)

    print(f"Felt array ({len(felt_array)} elements):")
    for i, felt in enumerate(felt_array):
        print(f"  [{i}]: {felt}")

    print()
    print("Serialization completed successfully!")


if __name__ == "__main__":
    main()