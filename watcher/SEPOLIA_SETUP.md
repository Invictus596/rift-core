# Sepolia Deployment - Complete Guide

## Current Status

⚠️ **RPC Network Issues Detected**

Starknet Sepolia RPC endpoints are currently experiencing issues. When resolved, follow the steps below.

---

## Your New Sepolia Account (Ready to Deploy)

I've created a new account configuration for you:

**Account File**: `/home/invictus/.starkli-wallets/sepolia-simple/account.json`

**Private Key**: `0x02021f31b175f39366e3ab37f0519ca7de31bc56e2a1d1f111c7bf0eb16f3e96`

**Public Key**: `0x008965d5def19c561bb580f6c40a537c7bc071c6f03dfe2c8cb85e8ee91db730`

⚠️ **SECURITY WARNING**: This private key is stored in plain text. Only use this for testnet development!

---

## Step-by-Step Deployment (When RPC is Working)

### Step 1: Get Your Account Address

```bash
starkli account oz init \
    --public-key 0x008965d5def19c561bb580f6c40a537c7bc071c6f03dfe2c8cb85e8ee91db730 \
    --salt 0x1
```

Copy the address output - you'll need it for the faucet.

### Step 2: Get Sepolia ETH

Visit one of these faucets and request test ETH:

1. **Primary**: https://starknet-faucet.vercel.app/
2. **Alternative**: https://faucet.sepolia.starknet.io/

Wait 1-2 minutes for confirmation.

### Step 3: Verify Balance (Optional)

```bash
export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/sepolia-simple/account.json
export STARKNET_PRIVATE_KEY=0x02021f31b175f39366e3ab37f0519ca7de31bc56e2a1d1f111c7bf0eb16f3e96

starkli balance --network sepolia YOUR_ACCOUNT_ADDRESS
```

### Step 4: Deploy Account

```bash
export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/sepolia-simple/account.json
export STARKNET_PRIVATE_KEY=0x02021f31b175f39366e3ab37f0519ca7de31bc56e2a1d1f111c7bf0eb16f3e96

starkli account deploy --network sepolia $STARKNET_ACCOUNT
```

Wait for transaction confirmation (1-2 minutes).

### Step 5: Deploy Verifier Contract

```bash
cd ~/rift-core-internal

export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/sepolia-simple/account.json
export STARKNET_PRIVATE_KEY=0x02021f31b175f39366e3ab37f0519ca7de31bc56e2a1d1f111c7bf0eb16f3e96

./watcher/deploy-sepolia.sh
```

---

## Alternative: Use Existing Account

If you prefer to use your existing deployer account:

```bash
# You'll need to enter the keystore password interactively
export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/deployer/burner_account.json
export STARKNET_KEYSTORE=/home/invictus/.starkli-wallets/deployer/burner_key.json

# Run in your local terminal where password prompts work
starkli account deploy --network sepolia $STARKNET_ACCOUNT
```

---

## Troubleshooting RPC Issues

### Check RPC Status

```bash
# Test Blast RPC
curl -X POST https://starknet-sepolia.public.blastapi.io \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"starknet_chainId","params":[],"id":1}'

# Test Starkware RPC  
curl -X POST https://free.rpc.sepolia.starknet.io/rpc/v0_7 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"starknet_chainId","params":[],"id":1}'
```

### Try Different RPC Endpoints

If one doesn't work, try another:

```bash
# Blast (free tier)
starkli account deploy --rpc https://starknet-sepolia.public.blastapi.io ...

# Nethermind
starkli account deploy --rpc https://rpc.sepolia.starknet.io/v1 ...

# Infura (requires API key)
starkli account deploy --rpc https://starknet-sepolia.infura.io/v3/YOUR_KEY ...
```

### Check Network Status

- **Starknet Status**: https://status.starknet.io/
- **Starkscan Sepolia**: https://sepolia.starkscan.co/

---

## After Successful Deployment

Once deployed, you'll get:
- **Contract Address**: `0x...`
- **Class Hash**: `0x...`

Update your watcher configuration:

```python
# watcher/watcher.py
STARKNET_RPC_MODE = True
KATANA_RPC_URL = "https://starknet-sepolia.public.blastapi.io"
VERIFIER_CONTRACT_ADDRESS = "0x..."  # Your deployed contract
```

Then run:
```bash
python watcher/watcher.py
```

---

## Resources

- **Starknet Sepolia Faucet**: https://starknet-faucet.vercel.app/
- **Starkscan Sepolia Explorer**: https://sepolia.starkscan.co/
- **Voyager Sepolia Explorer**: https://sepolia.voyager.online/
- **Starkli Book**: https://book.starkli.rs/
