# Rift Watcher - Python to Starknet Bridge

Monitor Bitcoin mempool for RIFT protocol transactions and submit proofs to Starknet.

---

## Quick Start

### Option 1: Mock Mode (No Blockchain)

Fastest way to test the watcher without any blockchain setup:

```bash
cd /home/invictus/rift-core-internal
source .venv/bin/activate
python watcher/watcher.py
```

### Option 2: Starknet Sepolia Testnet (Recommended for Production)

Deploy to real Starknet testnet for full integration testing:

**🚀 Fastest Path (5 minutes)**: See [QUICK_START.md](QUICK_START.md)

**Summary**:
```bash
# 1. Get free Alchemy RPC: https://www.alchemy.com/
#    - Create app → Starknet → Sepolia
#    - Copy your HTTPS RPC URL

# 2. Set your RPC URL
export ALCHEMY_RPC="https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_9/YOUR_KEY"

# 3. Deploy everything
./watcher/deploy-with-alchemy.sh

# 4. Configure and run watcher
# Set VERIFIER_CONTRACT_ADDRESS from deploy output
python watcher/watcher.py
```

**Full Guide**: [DEPLOYMENT_SEPOLIA.md](DEPLOYMENT_SEPOLIA.md)

### Option 3: Local Katana (Currently Blocked)

⚠️ **Known Issue**: Version incompatibility between Katana and starkli/starknet.py prevents local deployment.

See [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md) for details.

---

## Configuration

---

## Configuration

### Environment Variables

You can configure the bridge using environment variables:

```bash
export KATANA_RPC_URL="http://localhost:5050"
export KATANA_ACCOUNT_ADDRESS="0x127fd5f2f9c6f5a0d6f5e5c5b5a5f5e5d5c5b5a5f5e5d5c5b5a5f5e5d5c5b5a5"
export KATANA_PRIVATE_KEY="0x71d7bb07b9a64f6f78ac4c816aff4da9"
export VERIFIER_CONTRACT_ADDRESS="0x..."
```

### Watcher Configuration

Edit `watcher.py` to configure:

| Variable | Default | Description |
|----------|---------|-------------|
| `MOCK_MODE` | `True` | Generate mock Bitcoin transactions |
| `STARKNET_RPC_MODE` | `False` | Enable Starknet contract interaction |
| `POLL_INTERVAL` | `2` | Seconds between mempool polls |
| `RIFT_HEX_TAG` | `"52494654"` | Hex tag to detect ("RIFT") |

---

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Bitcoin Node   │────▶│ Rift Watcher │────▶│  Katana Node    │
│  (Mempool)      │     │  (Python)    │     │  (Starknet)     │
└─────────────────┘     └──────────────┘     └─────────────────┘
                              │                     │
                              │                     ▼
                              │            ┌─────────────────┐
                              │            │ Verifier        │
                              │            │ Contract        │
                              │            └─────────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ rpc_bridge.py│
                       │ (starknet.py)│
                       └──────────────┘
```

---

## Components

### `watcher.py`

Main mempool monitoring script:
- Polls Bitcoin mempool every 2 seconds
- Detects transactions with `OP_RETURN "RIFT"` tag
- Extracts transaction data
- Calls Starknet Verifier contract (when enabled)

### `rpc_bridge.py`

Starknet RPC communication layer:
- Account management and signing
- Contract declaration and deployment
- Function invocation (`verify_secp256k1_signature`)
- State queries (`is_verified`, `get_verification_count`)

### `serializer.py`

Data serialization utilities:
- Converts hex strings to Cairo field elements (felts)
- Handles 31-byte chunking for felt252 compatibility

### `test_rpc_bridge.py`

Integration test script:
- Tests full pipeline from account setup to contract interaction
- Validates contract deployment
- Provides deployed contract address for production use

---

## Testing

### Unit Test Serializer

```bash
python serializer.py
```

### Integration Test

```bash
# Start Katana first
katana --validate-max-steps 4000000 --invoke-max-steps 4000000

# Run test
python test_rpc_bridge.py
```

### Mock Mode Test

```bash
# watcher.py with MOCK_MODE=True
python watcher.py
```

---

## Troubleshooting

### "Connection refused" to Katana

Make sure Katana is running:
```bash
pgrep -x katana
```

### Contract not found

Build the contracts:
```bash
cd ../contracts && scarb build
```

### Account balance issues

Katana provides pre-funded accounts by default. Check the Katana output for account credentials.

### starknet.py import errors

Reinstall dependencies:
```bash
pip install -r ../requirements.txt
```

---

## Next Steps

1. **Deploy to Testnet**: Replace Katana with Starknet Sepolia testnet
2. **Signature Extraction**: Implement real secp256k1 signature extraction from Bitcoin transactions
3. **Mock to Real Verification**: Update `verifier.cairo` to use native secp256k1 precompiles
4. **Executor Contract**: Build the Executor contract to mint assets based on verified transactions

---

## License

MIT
