#!/bin/bash
# Deploy the Verifier contract to Katana using starkli
# This script handles the full deployment process

set -e

CONTRACT_PATH="/home/invictus/rift-core-internal/contracts/target/dev/rift_verifier_Verifier.contract_class.json"
ACCOUNT_FILE="/home/invictus/rift-core-internal/.starkli-accounts/katana-account.json"
KATANA_RPC="http://localhost:5050"

# Katana default account #0 credentials
ACCOUNT_ADDRESS="0x6162896d1d7ab204c7ccac6dd5f8e9e7c3eab1d1a1e1e1e1e1e1e1e1e1e1e1e"
PRIVATE_KEY="0xe177350e0334a19b5a1f5a0e86d113a022bbf6aa179ac3889007479a901e2cd"

echo "============================================================"
echo "RIFT Protocol - Verifier Contract Deployment"
echo "============================================================"
echo

# Check if Katana is running
echo "[*] Checking Katana connection..."
if ! curl -s "$KATANA_RPC" -X POST \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"starknet_chainId","params":[],"id":1}' | grep -q "result"; then
    echo "✗ Katana is not running at $KATANA_RPC"
    echo
    echo "Start Katana first:"
    echo "  katana --validate-max-steps 4000000 --invoke-max-steps 4000000"
    exit 1
fi
echo "✓ Katana is running"
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

# Step 1: Declare the contract
echo "[1/2] Declaring contract..."
DECLARE_OUTPUT=$(starkli declare \
    --rpc="$KATANA_RPC" \
    --account="$ACCOUNT_FILE" \
    --private-key="$PRIVATE_KEY" \
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
DEPLOY_OUTPUT=$(starkli deploy \
    --rpc="$KATANA_RPC" \
    --account="$ACCOUNT_FILE" \
    --private-key="$PRIVATE_KEY" \
    "$CLASS_HASH" \
    "$ACCOUNT_ADDRESS" 2>&1) || true

echo "$DEPLOY_OUTPUT"

# Extract contract address from output
CONTRACT_ADDR=$(echo "$DEPLOY_OUTPUT" | grep -oP "0x[0-9a-fA-F]{64}" | tail -1)

echo
echo "============================================================"
if [[ "$CONTRACT_ADDR" =~ ^0x[0-9a-fA-F]{64}$ ]]; then
    echo "✓ Contract deployed successfully!"
    echo "============================================================"
    echo
    echo "Contract Address: $CONTRACT_ADDR"
    echo "Class Hash: $CLASS_HASH"
    echo
    echo "To use this in watcher.py, set:"
    echo "  VERIFIER_CONTRACT_ADDRESS = \"$CONTRACT_ADDR\""
    echo "  STARKNET_RPC_MODE = True"
    echo
    echo "Then run:"
    echo "  python watcher/watcher.py"
else
    echo "✗ Deployment may have failed"
    echo "============================================================"
    echo
    echo "Check the error message above for details"
    echo "Deploy output: $DEPLOY_OUTPUT"
fi
