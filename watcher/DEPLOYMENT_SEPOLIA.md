# Deploy to Starknet Sepolia Testnet

Deploy your Verifier contract to Starknet's public testnet for real integration testing.

---

## Prerequisites

### 1. Install starkli (if not already installed)

```bash
curl https://get.starkli.sh | sh
starkliup
```

### 2. Get Sepolia ETH

You'll need Sepolia ETH for deployment (gas fees):

1. **Starknet Sepolia Faucet**: https://starknet-faucet.vercel.app/
2. **Alternative**: https://faucet.sepolia.starknet.io/

Enter your wallet address and request tokens (~0.1 ETH should be enough).

---

## Setup Sepolia Account

### Option A: Create New Account with starkli

```bash
# Create a new account directory
mkdir -p ~/.starkli-wallets/sepolia-account

# Generate a new signer (keystore will be created)
starkli signer generate keystore ~/.starkli-wallets/sepolia-account/keystore.json

# This will:
# 1. Ask you to set a password for the keystore
# 2. Display your public key - SAVE THIS!

# Create account config file
cat > ~/.starkli-wallets/sepolia-account/account.json << EOF
{
  "version": 1,
  "variant": {
    "type": "open_zeppelin",
    "version": 1,
    "public_key": "YOUR_PUBLIC_KEY_FROM_ABOVE"
  }
}
EOF
```

### Option B: Use Existing Account

If you already have a Sepolia account (e.g., from Braavos/ArgentX):

1. Export your private key or use the wallet's starkli compatibility mode
2. Create the account JSON file with your public key

---

## Fund Your Account

Verify your account has Sepolia ETH:

```bash
# Set environment variables
export STARKNET_ACCOUNT=~/.starkli-wallets/sepolia-account/account.json
export STARKNET_KEYSTORE=~/.starkli-wallets/sepolia-account/keystore.json

# Check balance (you'll be prompted for keystore password)
starkli balance --network sepolia $(starkli account address $STARKNET_ACCOUNT)
```

If balance is 0, get test ETH from the faucets above.

---

## Deploy the Contract

### Quick Deploy

```bash
cd /home/invictus/rift-core-internal

# Set environment variables
export STARKNET_ACCOUNT=~/.starkli-wallets/sepolia-account/account.json
export STARKNET_KEYSTORE=~/.starkli-wallets/sepolia-account/keystore.json

# Run deployment script
chmod +x watcher/deploy-sepolia.sh
./watcher/deploy-sepolia.sh
```

### Manual Deploy

```bash
# Declare contract
CLASS_HASH=$(starkli declare \
    --network sepolia \
    contracts/target/dev/rift_verifier_Verifier.contract_class.json)

# Get your account address
ACCOUNT_ADDR=$(starkli account address $STARKNET_ACCOUNT)

# Deploy contract
CONTRACT_ADDR=$(starkli deploy \
    --network sepolia \
    $CLASS_HASH \
    $ACCOUNT_ADDR)

echo "Contract deployed at: $CONTRACT_ADDR"
```

---

## Configure Watcher

After deployment, update `watcher/watcher.py`:

```python
# Starknet RPC Configuration
STARKNET_RPC_MODE = True
KATANA_RPC_URL = "https://starknet-sepolia.public.blastapi.io"
VERIFIER_CONTRACT_ADDRESS = "0x..."  # Your deployed contract address
```

Or use environment variables:

```bash
export STARKNET_RPC_MODE=true
export KATANA_RPC_URL="https://starknet-sepolia.public.blastapi.io"
export VERIFIER_CONTRACT_ADDRESS="0x..."
```

---

## Verify Deployment

### View on Block Explorers

- **Starkscan Sepolia**: https://sepolia.starkscan.co/contract/YOUR_CONTRACT_ADDRESS
- **Voyager Sepolia**: https://sepolia.voyager.online/contract/YOUR_CONTRACT_ADDRESS

### Test Contract Interaction

```bash
# Call is_verified (should return false for unverified tx)
starkli call \
    --network sepolia \
    $CONTRACT_ADDR \
    is_verified \
    0x1234567890abcdef

# Call get_verification_count (should return 0 initially)
starkli call \
    --network sepolia \
    $CONTRACT_ADDR \
    get_verification_count

# Call get_owner
starkli call \
    --network sepolia \
    $CONTRACT_ADDR \
    get_owner
```

---

## Run the Watcher with Sepolia

```bash
cd /home/invictus/rift-core-internal
source .venv/bin/activate

# Make sure environment variables are set
export STARKNET_RPC_MODE=true
export KATANA_RPC_URL="https://starknet-sepolia.public.blastapi.io"
export VERIFIER_CONTRACT_ADDRESS="0x..."

# Run watcher
python watcher/watcher.py
```

---

## Cost Estimate

Deployment costs (approximate, varies with gas prices):

| Operation | Cost (Sepolia ETH) | Cost (USD) |
|-----------|-------------------|------------|
| Declare Contract | ~0.001 - 0.005 | $0 (testnet) |
| Deploy Contract | ~0.0001 - 0.001 | $0 (testnet) |
| Verify Signature | ~0.00001 - 0.0001 | $0 (testnet) |

**Total**: ~0.001 - 0.006 Sepolia ETH per full deployment

---

## Troubleshooting

### "Account not deployed"

Your account needs to be deployed first:

```bash
starkli account deploy \
    --network sepolia \
    $STARKNET_ACCOUNT
```

### "Insufficient balance"

Get more Sepolia ETH from faucets or wait for faucet cooldown.

### "Transaction timeout"

Sepolia can be slow. Wait a few minutes and check the transaction on Starkscan.

### "Class hash already declared"

The contract was already declared. Use the existing class hash and just deploy:

```bash
starkli deploy --network sepolia YOUR_CLASS_HASH YOUR_ACCOUNT_ADDRESS
```

---

## Next Steps

1. ✅ Deploy contract to Sepolia
2. ✅ Configure watcher with contract address
3. ✅ Test with mock Bitcoin transactions
4. ⏭️ Implement real signature extraction
5. ⏭️ Build Executor contract

---

## Resources

- [Starknet Sepolia Docs](https://docs.starknet.io/documentation/develop/Networks/sepolia-testnet/)
- [starkli Book](https://book.starkli.rs/)
- [Starkscan Sepolia](https://sepolia.starkscan.co/)
- [Starknet Faucet](https://starknet-faucet.vercel.app/)
