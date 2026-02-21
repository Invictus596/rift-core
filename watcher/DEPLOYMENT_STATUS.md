# Deployment Status & Known Issues

## Current Status

✅ **Watcher (Bitcoin)**: Fully functional in mock mode
✅ **Verifier Contract**: Compiles successfully with Cairo 2.6.4
✅ **RPC Bridge Code**: Complete and ready for integration
⚠️ **Contract Deployment**: Blocked by tooling version incompatibility

## Known Issue: Katana/starkli/starknet.py Version Mismatch

### Problem

The local Katana node uses non-standard block tags (`l1_accepted`, `latest`, `pre_confirmed`) while the current versions of starkli (0.4.2) and starknet.py (0.23.0) expect the standard Starknet tag (`pending`).

This causes all deployment attempts to fail with:
```
JSON-RPC error: code=-32602, message="Invalid params", 
data="unknown variant `pending`, expected one of `l1_accepted`, `latest`, `pre_confirmed`"
```

### Affected Components

- `starkli declare/deploy` commands
- `starknet.py` Account operations
- Any tool using the standard Starknet JSON-RPC spec

### Workarounds

#### Option 1: Use Mock Mode (Recommended for Development)

The watcher works perfectly in mock mode without needing Starknet:

```bash
python watcher/watcher.py
```

This will:
- Generate mock Bitcoin transactions
- Detect RIFT tags
- Log all activity
- Skip Starknet contract calls

#### Option 2: Deploy to Starknet Testnet

Deploy to Starknet Sepolia testnet instead of local Katana:

```bash
# Using starkli with testnet
starkli declare \
    --network sepolia \
    --account ~/.starkli-wallets/<your-account>/account.json \
    --keystore ~/.starkli-wallets/<your-account>/keystore.json \
    contracts/target/dev/rift_verifier_Verifier.contract_class.json
```

#### Option 3: Use Compatible Katana Version

Try an older version of Katana that supports the `pending` block tag, or wait for starkli/starknet.py to add support for Katana's custom block tags.

### Files Ready for Deployment

Once the version issue is resolved, use:

```bash
# Deploy script (requires compatible Katana)
./watcher/deploy.sh

# Manual deployment
starkli declare \
    --rpc=http://localhost:5050 \
    --account=./.starkli-accounts/katana-account.json \
    --private-key=0xe177350e0334a19b5a1f5a0e86d113a022bbf6aa179ac3889007479a901e2cd \
    contracts/target/dev/rift_verifier_Verifier.contract_class.json
```

## Next Steps

1. **For Now**: Continue development in mock mode
2. **Monitor**: Watch for starkli/starknet.py updates with Katana compatibility
3. **Alternative**: Consider deploying to Starknet Sepolia testnet for integration testing
4. **Long-term**: Plan migration to standard Starknet-compatible RPC node

## Contact

For updates on this issue, check:
- [starkli GitHub](https://github.com/foundry-rs/starkli)
- [starknet.py GitHub](https://github.com/software-mansion/starknet.py)
- [Katana GitHub](https://github.com/dojoengine/dojo)
