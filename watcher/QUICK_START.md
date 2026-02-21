# 🚀 Quick Start: Deploy to Sepolia with Alchemy

## 5-Minute Setup Guide

### Step 1: Get Free Alchemy RPC (3 minutes)

1. **Sign Up**: https://www.alchemy.com/
   - Use GitHub/Google for instant signup

2. **Create App**: 
   - Click "Create App"
   - Chain: **Starknet**
   - Network: **Sepolia** (testnet)
   - Name: **Rift Protocol**

3. **Copy RPC URL**:
   - Go to your app's "API KEYS" tab
   - Copy the **HTTPS** URL for Sepolia
   - Looks like: `https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_9/your-key-here`

### Step 2: Deploy Everything (2 minutes)

```bash
# 1. Set your Alchemy RPC URL
export ALCHEMY_RPC="YOUR_RPC_URL_HERE"

# 2. Run the deployment script
cd ~/rift-core-internal
./watcher/deploy-with-alchemy.sh
```

That's it! The script will:
- ✅ Deploy your account (if needed)
- ✅ Deploy the Verifier contract
- ✅ Give you the contract address
- ✅ Show you how to configure the watcher

---

## After Deployment

Update your `watcher/watcher.py`:

```python
STARKNET_RPC_MODE = True
KATANA_RPC_URL = "YOUR_ALCHEMY_RPC_URL"
VERIFIER_CONTRACT_ADDRESS = "0x..."  # From script output
```

Then run:
```bash
python watcher/watcher.py
```

---

## Get Sepolia ETH (If Needed)

If the script says "Insufficient funds":

1. Copy your account address from the script output
2. Visit: https://starknet-faucet.vercel.app/
3. Paste your address and request test ETH
4. Wait 1-2 minutes
5. Re-run the deployment script

---

## Troubleshooting

### "Invalid RPC URL"
- Make sure you copied the full URL including `/rpc/v0_9/`
- Check there are no trailing spaces

### "Account already deployed"
- This is good! The script will skip account deployment
- Just need to get Sepolia ETH if balance is 0

### "Class hash already declared"
- The contract was already declared
- Script will still deploy a new instance

### Still stuck?
- Check Alchemy dashboard for API errors
- Try refreshing your RPC key in Alchemy dashboard
- Join Starknet Discord: https://discord.gg/starknet

---

## What You Get

✅ **Dedicated RPC** - No rate limits (3M compute units/month free)
✅ **Latest RPC Spec** - Full compatibility with starkli
✅ **Reliable** - 99.9% uptime
✅ **Free** - No credit card needed

---

## Resources

- **Alchemy Dashboard**: https://dashboard.alchemy.com/
- **Starkscan Explorer**: https://sepolia.starkscan.co/
- **Starknet Faucet**: https://starknet-faucet.vercel.app/
- **Starkli Docs**: https://book.starkli.rs/
