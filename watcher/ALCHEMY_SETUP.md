# Quick Setup: Alchemy Free RPC (5 minutes)

Public RPCs are congested or incompatible. Get your own free dedicated RPC:

## Step 1: Sign Up for Alchemy (2 minutes)

1. Go to: https://www.alchemy.com/
2. Click "Sign Up Free" (GitHub/Google/Email)
3. Complete signup

## Step 2: Create Starknet App (1 minute)

1. Click "Create App" button
2. **Chain**: Starknet
3. **Network**: Sepolia (testnet)
4. **Name**: Rift Protocol (or anything)
5. Click "Create App"

## Step 3: Get Your RPC URL (30 seconds)

1. Click on your newly created app
2. Go to "API KEYS" tab
3. Copy the **HTTPS** URL under "Sepolia"

It will look like:
```
https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_9/YOUR_API_KEY
```

## Step 4: Deploy Your Account

```bash
# Set your Alchemy RPC URL
export ALCHEMY_RPC="https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_9/YOUR_API_KEY"

# Export account credentials
export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/sepolia-simple/account.json
export STARKNET_PRIVATE_KEY=0x02021f31b175f39366e3ab37f0519ca7de31bc56e2a1d1f111c7bf0eb16f3e96

# Deploy account
starkli account deploy --rpc $ALCHEMY_RPC $STARKNET_ACCOUNT

# Once deployed, deploy the Verifier contract
cd ~/rift-core-internal
./watcher/deploy-sepolia.sh
```

---

## Why This Works Better

✅ **Dedicated RPC** - No rate limits or congestion
✅ **Latest Spec** - Alchemy supports latest JSON-RPC spec
✅ **Free Tier** - 3M compute units/month (plenty for development)
✅ **Reliable** - 99.9% uptime SLA

---

## Alternative: Infura

If you prefer Infura:

1. Sign up: https://www.infura.io/
2. Create Starknet Sepolia endpoint
3. Use the JSON-RPC URL

---

## Troubleshooting

### "Account already deployed"

Your account is already deployed! Check the balance:

```bash
starkli balance --rpc $ALCHEMY_RPC YOUR_ACCOUNT_ADDRESS
```

### "Insufficient funds"

Get Sepolia ETH from:
- https://starknet-faucet.vercel.app/
- https://faucet.sepolia.starknet.io/

### Still getting errors

Try the v0_7 endpoint:
```bash
export ALCHEMY_RPC="https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_7/YOUR_API_KEY"
```
