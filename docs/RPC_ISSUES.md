# RPC Compatibility Issues - Sepolia & Katana

## Summary

**Both Sepolia RPC (v0.10+) and Katana (v1.7.1) are incompatible with starkli 0.4.2** due to their handling of the "pending" block tag. This blocks on-chain deployment and testing.

---

## Issue 1: Alchemy Sepolia RPC v0.10+

### Problem
Starkli 0.4.2 uses the "pending" block tag when checking account state, but Alchemy's Sepolia RPC v0.10 doesn't support this tag.

### Error Message
```
Error: RPC error: ErrorObject { code: ServerError(-32602), message: "Invalid params", data: Some(String("Invalid block id")) }
```

### Root Cause
When deploying an account, starkli calls `starknet_getNonce` with block tag `"pending"`:
```json
{"method": "starknet_getNonce", "params": ["pending", "0x..."]}
```

Alchemy's RPC responds:
```json
{"error": {"code": -32602, "message": "Invalid params", "reason": "Invalid block id"}}
```

### Test Results
| Block Tag | Response |
|-----------|----------|
| `"pending"` | ❌ "Invalid block id" |
| `"latest"` | ✅ "Contract not found" (expected for undeployed account) |

### Attempted Solutions

#### ✅ RPC v0.8 Endpoint (Partial Success)
Using RPC v0.8 instead of v0.10:
```bash
export ALCHEMY_RPC="https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_8/YOUR_KEY"
```

**Status**: Account creation works, but deployment still fails with nonce errors.

#### ❌ Alternative RPCs
- `https://rpc.sepolia.starknet.io/rpc/v0_8` - Same issue
- `https://starknet-sepolia.public.blastapi.io/rpc/v0_8` - Rate limited + pending issues

---

## Issue 2: Katana Local Node

### Problem
Katana 1.7.1 also doesn't support the "pending" block tag, making local development impossible.

### Error Message
```
Error: RPC error: ErrorObject { code: ServerError(-32602), message: "Invalid params", data: Some(String("Invalid block id")) }
```

### Root Cause
Same as Sepolia - Katana's RPC implementation doesn't fully support the "pending" block tag that starkli requires.

### Attempted Solutions

#### ❌ Katana Flags
```bash
# Tried various combinations - all fail on "pending" tag
katana --validate-max-steps 4000000 --invoke-max-steps 4000000
katana --disable-fee
katana --allow-zero-overrides
```

#### ❌ Different Katana Versions
- v1.6.x - Same issue
- v1.7.1 - Same issue

---

## Why This Happens

Starkli 0.4.2 assumes all RPCs support the "pending" block tag per Starknet RPC spec 0.8.1+. However:

1. **RPC providers have limited "pending" support** - Many don't implement it fully
2. **Spec vs Implementation gap** - The spec says "should support", but providers interpret differently
3. **Starkli doesn't gracefully degrade** - No fallback to "latest" when "pending" fails

---

## Impact on Development

| Component | Status | Reason |
|-----------|--------|--------|
| Watcher Code | ✅ Working | Pure Python, no RPC needed |
| Verifier Contract | ✅ Compiles | Cairo build works fine |
| RPC Bridge | ✅ Complete | starknet.py integration ready |
| Account Deployment | ❌ Blocked | starkli requires "pending" tag |
| Contract Deployment | ❌ Blocked | Requires deployed account |
| End-to-End Testing | ❌ Blocked | Cannot deploy to testnet or local |

---

## Workarounds

### ✅ Option 1: Mock Mode (Recommended for Now)

The watcher works perfectly in mock mode without Starknet deployment:

```bash
cd ~/rift-core-internal
source .venv/bin/activate
python watcher/watcher.py
```

**Pros**:
- Full pipeline demonstration
- No RPC dependencies
- Reliable and reproducible
- Perfect for hackathons/demos

**Cons**:
- No actual Starknet verification
- Mock signatures (not real crypto)

### ⚠️ Option 2: Patch Starkli (Advanced)

Modify starkli's source to use "latest" instead of "pending":

```bash
# Clone starkli repo
git clone https://github.com/foundry-rs/starkli
cd starkli

# Find and patch the block tag logic in crates/starknet-rpc/src/lib.rs
# Change "pending" to "latest" for undeployed accounts

# Rebuild
cargo build --release
```

**Status**: Not attempted - time consuming, breaks with updates

### ⚠️ Option 3: Use Pre-deployed Account

If you have an already-deployed account from a different tool:

```bash
export STARKNET_ACCOUNT=/path/to/deployed-account.json
export STARKNET_PRIVATE_KEY=0x...

# This works because starkli won't call getNonce for deployed accounts
starkli declare --rpc $ALCHEMY_RPC ...
```

**Status**: Requires external deployment method

### ⚠️ Option 4: Different Deployment Tool

Try **Brazos**, **Starknet.js**, or **Hardhat Starknet**:

```bash
# Using starknet.js (example)
npm install starknet
# Write deployment script in JavaScript
```

**Status**: Requires rewriting deployment scripts

### ⚠️ Option 5: Manual Wallet Deployment

Deploy account via UI wallet, then use starkli for contracts:

1. Install **Braavos** or **Argent X** wallet
2. Create account on Sepolia testnet
3. Export account for starkli use

**Status**: Possible but complex workflow

---

## Current Status (Hackathon Ready)

We're proceeding with **Mock Mode** for the hackathon:

```bash
# Run the hackathon demo
./watcher/run-hackathon-demo.sh
```

This demonstrates:
- ✅ Bitcoin mempool monitoring
- ✅ RIFT tag detection
- ✅ Transaction parsing
- ✅ RPC Bridge architecture (ready for integration)

---

## Tracking & References

- **starkli GitHub**: https://github.com/foundry-rs/starkli/issues
- **Katana GitHub**: https://github.com/dojoengine/dojo/issues
- **Alchemy Status**: https://status.alchemy.com/
- **Starknet RPC Spec**: https://github.com/starkware-libs/starknet-specs
- **RPC v0.8 Spec**: https://github.com/starkware-libs/starknet-specs/releases/tag/v0.8.1

---

## Timeline

| Date | Event |
|------|-------|
| Feb 19, 2026 | Discovered Sepolia RPC v0.10 "pending" tag issue |
| Feb 19, 2026 | Tried RPC v0.8 endpoint - partial success |
| Feb 19, 2026 | Created Sepolia account - awaiting faucet |
| Feb 20, 2026 | Mock mode testing complete (20 cycles, 28 txs detected) |
| Feb 20, 2026 | Katana testing - same "pending" tag issue |
| Feb 21, 2026 | Decision: Proceed with mock mode for hackathon |

---

## Resolution Path

**Short-term (Hackathon)**:
- ✅ Mock mode demonstration
- ✅ Full pipeline architecture demo
- ⏸️ On-chain verification pending

**Long-term**:
1. Wait for starkli fix (track GitHub issues)
2. Wait for RPC providers to add "pending" support
3. Consider alternative deployment tools
4. Potential starkli fork/patch if critical

---

## Contact & Support

If you've solved this issue or have insights:
- Open a GitHub issue
- Share your workaround in the docs
- Contact: Rift Protocol Team
