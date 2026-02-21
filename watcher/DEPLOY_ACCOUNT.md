# Deploy Your Account to Sepolia - Manual Steps

Your starkli account is configured but not yet deployed to Sepolia.

## Your Account Info

```
Config File: /home/invictus/.starkli-wallets/deployer/burner_account.json
Keystore: /home/invictus/.starkli-wallets/deployer/burner_key.json
Public Key: 0x14e002d131a01501f02c4173a00b1bf1295e7f9890eaf77c1cf6a59cad5420d
Class Hash: 0x5b4b537eaa2399e3aa99c4e2e0208ebd6c71bc1467938cd52c798c601e43564
Salt: 0x2ebef6509673486dafad042b38f88c3800e70bf4235355967234ae4e23b9ba2
```

## Step 1: Get Your Account Address

Run this command to calculate your future account address:

```bash
starkli account oz init \
    --public-key 0x14e002d131a01501f02c4173a00b1bf1295e7f9890eaf77c1cf6a59cad5420d \
    --salt 0x2ebef6509673486dafad042b38f88c3800e70bf4235355967234ae4e23b9ba2
```

Copy the address - you'll need it for the faucet.

## Step 2: Get Sepolia ETH

Visit one of these faucets and request test ETH for your account address:

1. **Primary**: https://starknet-faucet.vercel.app/
2. **Alternative**: https://faucet.sepolia.starknet.io/

**Note**: Faucets typically give 0.1 - 1 Sepolia ETH. Wait for confirmation.

## Step 3: Deploy Account

Run this command (you'll be prompted for your keystore password):

```bash
export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/deployer/burner_account.json
export STARKNET_KEYSTORE=/home/invictus/.starkli-wallets/deployer/burner_key.json

starkli account deploy --network sepolia $STARKNET_ACCOUNT
```

**Enter your keystore password** when prompted.

Wait for the transaction to confirm (1-2 minutes).

## Step 4: Verify Deployment

Check that your account is deployed:

```bash
# Check balance
starkli balance --network sepolia YOUR_ACCOUNT_ADDRESS

# Or check on Starkscan
# https://sepolia.starkscan.co/contract/YOUR_ACCOUNT_ADDRESS
```

## Step 5: Deploy Verifier Contract

Once your account is deployed and funded, run:

```bash
cd /home/invictus/rift-core-internal
export STARKNET_ACCOUNT=/home/invictus/.starkli-wallets/deployer/burner_account.json
export STARKNET_KEYSTORE=/home/invictus/.starkli-wallets/deployer/burner_key.json

./watcher/deploy-sepolia.sh
```

---

## Alternative: Use Private Key Directly

If you know your private key, you can skip the keystore password prompt:

```bash
# WARNING: Only do this in secure environments
export STARKNET_PRIVATE_KEY=your_private_key_here

starkli account deploy \
    --network sepolia \
    --private-key $STARKNET_PRIVATE_KEY \
    /home/invictus/.starkli-wallets/deployer/burner_account.json
```

---

## Troubleshooting

### "Insufficient max fee"

Increase the gas limits:

```bash
starkli account deploy \
    --network sepolia \
    --l1-gas 100000 \
    --l1-gas-price 1000000000 \
    $STARKNET_ACCOUNT
```

### "Nonce too low" or "Account already deployed"

Your account is already deployed. Check the address on Starkscan.

### "Insufficient balance"

Wait for faucet confirmation or try the alternative faucet.
