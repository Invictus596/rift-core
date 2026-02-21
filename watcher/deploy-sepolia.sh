#!/bin/bash
# Deploy the Verifier contract to Starknet Sepolia Testnet
# Prerequisites:
#   - starkli installed
#   - Sepolia account configured (see setup instructions below)

set -e

CONTRACT_PATH="/home/invictus/rift-core-internal/contracts/target/dev/rift_verifier_Verifier.contract_class.json"
NETWORK="sepolia"

echo "============================================================"
echo "RIFT Protocol - Sepolia Testnet Deployment"
echo "============================================================"
echo

# Check if contract exists
echo "[*] Checking contract file..."
if [ ! -f "$CONTRACT_PATH" ]; then
    echo "✗ Contract not found: $CONTRACT_PATH"
    echo
    echo "Build the contract first:"
    echo "  cd contracts && scarb build"
    exit 1
fi
echo "✓ Contract found"
echo

# Check for account
echo "[*] Checking for Sepolia account..."
if [ -z "$STARKNET_ACCOUNT" ]; then
    echo "✗ STARKNET_ACCOUNT environment variable not set"
    echo
    echo "Set up your Sepolia account first (see DEPLOYMENT_SEPOLIA.md)"
    echo
    echo "Then run:"
    echo "  export STARKNET_ACCOUNT=/path/to/your/account.json"
    echo "  export STARKNET_KEYSTORE=/path/to/your/keystore.json"
    exit 1
fi

if [ -z "$STARKNET_KEYSTORE" ]; then
    echo "✗ STARKNET_KEYSTORE environment variable not set"
    echo
    echo "Set up your Sepolia account first (see DEPLOYMENT_SEPOLIA.md)"
    exit 1
fi

echo "✓ Account configured: $STARKNET_ACCOUNT"
echo

# Step 1: Declare the contract
echo "[1/2] Declaring contract on Sepolia..."
echo "    This may take 1-2 minutes for transaction confirmation"
echo

DECLARE_OUTPUT=$(starkli declare \
    --network="$NETWORK" \
    "$CONTRACT_PATH" 2>&1) || true

echo "$DECLARE_OUTPUT"

# Extract class hash from output
CLASS_HASH=$(echo "$DECLARE_OUTPUT" | grep -oP "0x[0-9a-fA-F]{64}" | head -1)

if [[ ! "$CLASS_HASH" =~ ^0x[0-9a-fA-F]{64}$ ]]; then
    echo
    echo "✗ Declaration failed"
    echo "Output: $DECLARE_OUTPUT"
    exit 1
fi

echo
echo "✓ Contract declared: $CLASS_HASH"
echo

# Step 2: Deploy the contract
echo "[2/2] Deploying contract..."
echo "    Constructor argument: your account address as owner"
echo

# Get account address
ACCOUNT_ADDR=$(starkli account address "$STARKNET_ACCOUNT" 2>/dev/null || echo "0x0")

DEPLOY_OUTPUT=$(starkli deploy \
    --network="$NETWORK" \
    "$CLASS_HASH" \
    "$ACCOUNT_ADDR" 2>&1) || true

echo "$DEPLOY_OUTPUT"

# Extract contract address from output
CONTRACT_ADDR=$(echo "$DEPLOY_OUTPUT" | grep -oP "0x[0-9a-fA-F]{64}" | tail -1)

echo
echo "============================================================"
if [[ "$CONTRACT_ADDR" =~ ^0x[0-9a-fA-F]{64}$ ]]; then
    echo "✓ Contract deployed successfully on Sepolia!"
    echo "============================================================"
    echo
    echo "Contract Address: $CONTRACT_ADDR"
    echo "Class Hash: $CLASS_HASH"
    echo
    echo "View on Starkscan:"
    echo "  https://sepolia.starkscan.co/contract/$CONTRACT_ADDR"
    echo
    echo "View on Voyager:"
    echo "  https://sepolia.voyager.online/contract/$CONTRACT_ADDR"
    echo
    echo "To use this in watcher.py, set:"
    echo "  STARKNET_RPC_MODE = True"
    echo "  KATANA_RPC_URL = \"https://starknet-sepolia.public.blastapi.io\""
    echo "  VERIFIER_CONTRACT_ADDRESS = \"$CONTRACT_ADDR\""
    echo
    echo "Then run:"
    echo "  python watcher/watcher.py"
    echo
    echo "============================================================"
else
    echo "✗ Deployment may have failed"
    echo "============================================================"
    echo
    echo "Check the error message above for details"
    echo "Deploy output: $DEPLOY_OUTPUT"
fi
