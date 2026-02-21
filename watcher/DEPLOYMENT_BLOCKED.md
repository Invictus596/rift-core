# Deployment Status - Starkli RPC Compatibility Issue

## Problem Summary

**Issue**: Starkli 0.4.2 uses the "pending" block tag when checking account state, but Alchemy's Sepolia RPC v0.10 doesn't support this tag, returning "Invalid block id" error.

## Root Cause

When deploying an account, starkli calls `starknet_getNonce` with block tag `"pending"`:
```json
{"method": "starknet_getNonce", "params": ["pending", "0x..."]}
```

Alchemy's RPC responds:
```json
{"error": {"code": -32602, "message": "Invalid params", "reason": "Invalid block id"}}
```

**Test Results**:
- `"pending"` → ❌ "Invalid block id"
- `"latest"` → ✅ "Contract not found" (expected for undeployed account)

## Why This Happens

Starkli 0.4.2 assumes all RPCs support the "pending" block tag per Starknet RPC spec 0.8.1+. However, many RPC providers (including Alchemy's v0.10) have limited or no support for "pending" queries.

## Workarounds

### Option 1: Use an RPC that Supports "pending" (Recommended)

Try these RPCs which may support the "pending" tag:

```bash
# Nethermind (official)
export ALCHEMY_RPC="https://rpc.sepolia.starknet.io/rpc/v0_8"

# Or wait for Alchemy to add pending support
```

### Option 2: Patch Starkli (Advanced)

Modify starkli's source to use "latest" instead of "pending" for undeployed accounts:
```bash
# Clone starkli repo
git clone https://github.com/foundry-rs/starkli
# Patch the block tag logic
# Rebuild
cargo build --release
```

### Option 3: Use a Pre-deployed Account

If you have an already-deployed account (from a previous session or different tool), you can use it:

```bash
# Account must already be deployed
export STARKNET_ACCOUNT=/path/to/deployed-account.json
export STARKNET_KEYSTORE=/path/to/keystore.json

# This works because starkli won't call getNonce for deployed accounts
starkli declare --rpc $ALCHEMY_RPC ...
```

### Option 4: Use a Different Deployment Tool

Try using **Brazos** or **Starknet.js** which might handle block tags differently:

```bash
# Using brazos CLI (if available)
brazos deploy account --network sepolia ...
```

### Option 5: Continue with Mock Mode

The watcher works perfectly in mock mode without Starknet deployment:

```bash
python watcher/watcher.py
```

## Current Status

| Component | Status |
|-----------|--------|
| Watcher Code | ✅ Complete |
| Verifier Contract | ✅ Compiles |
| RPC Bridge | ✅ Complete |
| Account Deployment | ❌ Blocked (starkli RPC bug) |
| Contract Deployment | ⏸️ Waiting on account |

## Recommended Path

**For Now**: Continue development in **mock mode**

**Long-term**: 
1. Wait for starkli fix (track issue on GitHub)
2. Or wait for Alchemy to add "pending" support
3. Or deploy to mainnet using a different toolchain

## Tracking

- **starkli GitHub**: https://github.com/foundry-rs/starkli
- **Alchemy Status**: https://status.alchemy.com/
- **Starknet RPC Spec**: https://github.com/starkware-libs/starknet-specs

## Alternative: Manual Deployment via UI

Some wallets support account deployment via UI:
- **Braavos**: https://braavos.app/
- **Argent X**: https://www.argent.xyz/

Deploy account via wallet, then use starkli for contract deployment.
