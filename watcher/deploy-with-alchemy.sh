#!/bin/bash
# Deploy to Sepolia using Alchemy RPC
# Prerequisites:
#   1. Free Alchemy account: https://www.alchemy.com/
#   2. Create Starknet Sepolia app
#   3. Get your RPC URL

set -e

echo "============================================================"
echo "RIFT Protocol - Alchemy Sepolia Deployment"
echo "============================================================"
echo

# Check for Alchemy RPC
if [ -z "$ALCHEMY_RPC" ]; then
    echo "❌ ALCHEMY_RPC environment variable not set"
    echo
    echo "📝 Quick Setup (5 minutes):"
    echo "  1. Sign up: https://www.alchemy.com/"
    echo "  2. Create App → Chain: Starknet → Network: Sepolia"
    echo "  3. Copy your HTTPS RPC URL"
    echo
    echo "🔧 Then run:"
    echo "  export ALCHEMY_RPC=\"https://starknet-sepolia.g.alchemy.com/starknet/version/rpc/v0_9/YOUR_KEY\""
    echo "  ./watcher/deploy-with-alchemy.sh"
    echo
    exit 1
fi

echo "✅ Using Alchemy RPC: ${ALCHEMY_RPC:0:50}..."
echo

# Test RPC connection
echo "[*] Testing RPC connection..."
CHAIN_ID=$(curl -s -X POST "$ALCHEMY_RPC" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","method":"starknet_chainId","params":[],"id":1}' \
    | jq -r '.result // empty')

if [ -z "$CHAIN_ID" ]; then
    echo "❌ Failed to connect to Alchemy RPC"
    echo "   Check your RPC URL is correct"
    exit 1
fi

echo "✅ Connected! Chain ID: $CHAIN_ID"
echo

# Account configuration
STARKNET_ACCOUNT="/home/invictus/.starkli-wallets/sepolia-simple/account.json"
STARKNET_PRIVATE_KEY="0x02021f31b175f39366e3ab37f0519ca7de31bc56e2a1d1f111c7bf0eb16f3e96"
CONTRACT_PATH="/home/invictus/rift-core-internal/contracts/target/dev/rift_verifier_Verifier.contract_class.json"

echo "============================================================"
echo "Step 1: Deploy Account"
echo "============================================================"
echo

# Check if account is already deployed
echo "[*] Checking account deployment status..."
ACCOUNT_CONFIG=$(cat $STARKNET_ACCOUNT | jq -r '.deployment.status')

if [ "$ACCOUNT_CONFIG" = "deployed" ]; then
    echo "✅ Account already deployed"
    ACCOUNT_ADDR=$(cat $STARKNET_ACCOUNT | jq -r '.deployment.address')
else
    echo "[*] Deploying account contract..."
    echo "    This will take 1-2 minutes..."
    echo
    
    DEPLOY_OUTPUT=$(starkli account deploy \
        --rpc="$ALCHEMY_RPC" \
        --private-key="$STARKNET_PRIVATE_KEY" \
        "$STARKNET_ACCOUNT" 2>&1) || DEPLOY_FAILED=true
    
    if [ "$DEPLOY_FAILED" = "true" ]; then
        echo "❌ Account deployment failed:"
        echo "$DEPLOY_OUTPUT"
        echo
        echo "💡 Possible solutions:"
        echo "   - Check you have Sepolia ETH: https://starknet-faucet.vercel.app/"
        echo "   - Try a different RPC version: v0_7 instead of v0_9"
        exit 1
    fi
    
    echo "$DEPLOY_OUTPUT"
    
    # Extract transaction hash
    TX_HASH=$(echo "$DEPLOY_OUTPUT" | grep -oP "0x[0-9a-fA-F]{64}" | head -1)
    echo
    echo "✅ Account deployed! Transaction: $TX_HASH"
    echo "   Waiting for confirmation..."
    sleep 30
fi

# Get account address
ACCOUNT_ADDR=$(starkli account address "$STARKNET_ACCOUNT" 2>/dev/null || \
               cat $STARKNET_ACCOUNT | jq -r '.deployment.address')

echo
echo "📍 Account Address: $ACCOUNT_ADDR"
echo

# Check balance
echo "[*] Checking account balance..."
BALANCE=$(starkli balance --rpc="$ALCHEMY_RPC" "$ACCOUNT_ADDR" 2>/dev/null || echo "0")
echo "   Balance: $BALANCE STRK"
echo

echo "============================================================"
echo "Step 2: Deploy Verifier Contract"
echo "============================================================"
echo

# Check if contract exists
if [ ! -f "$CONTRACT_PATH" ]; then
    echo "❌ Contract not found: $CONTRACT_PATH"
    echo
    echo "🔧 Build first:"
    echo "   cd contracts && scarb build"
    exit 1
fi

echo "[*] Declaring contract..."
DECLARE_OUTPUT=$(starkli declare \
    --rpc="$ALCHEMY_RPC" \
    --private-key="$STARKNET_PRIVATE_KEY" \
    "$CONTRACT_PATH" 2>&1) || DECLARE_FAILED=true

if [ "$DECLARE_FAILED" = "true" ]; then
    echo "❌ Declaration failed:"
    echo "$DECLARE_OUTPUT"
    exit 1
fi

echo "$DECLARE_OUTPUT"

# Extract class hash
CLASS_HASH=$(echo "$DECLARE_OUTPUT" | grep -oP "0x[0-9a-fA-F]{64}" | head -1)

if [[ ! "$CLASS_HASH" =~ ^0x[0-9a-fA-F]{64}$ ]]; then
    echo "❌ Failed to extract class hash"
    exit 1
fi

echo
echo "✅ Contract declared: $CLASS_HASH"
echo

echo "[*] Deploying contract instance..."
DEPLOY_OUTPUT=$(starkli deploy \
    --rpc="$ALCHEMY_RPC" \
    --private-key="$STARKNET_PRIVATE_KEY" \
    "$CLASS_HASH" \
    "$ACCOUNT_ADDR" 2>&1) || DEPLOY_FAILED=true

if [ "$DEPLOY_FAILED" = "true" ]; then
    echo "❌ Deployment failed:"
    echo "$DEPLOY_OUTPUT"
    exit 1
fi

echo "$DEPLOY_OUTPUT"

# Extract contract address
CONTRACT_ADDR=$(echo "$DEPLOY_OUTPUT" | grep -oP "0x[0-9a-fA-F]{64}" | tail -1)

echo
echo "============================================================"
echo "🎉 Deployment Successful!"
echo "============================================================"
echo
echo "📄 Contract Address: $CONTRACT_ADDR"
echo "📄 Class Hash: $CLASS_HASH"
echo "📄 Owner Account: $ACCOUNT_ADDR"
echo
echo "🔍 View on explorers:"
echo "   Starkscan: https://sepolia.starkscan.co/contract/$CONTRACT_ADDR"
echo "   Voyager:   https://sepolia.voyager.online/contract/$CONTRACT_ADDR"
echo
echo "🔧 Configure watcher.py:"
echo "   STARKNET_RPC_MODE = True"
echo "   KATANA_RPC_URL = \"$ALCHEMY_RPC\""
echo "   VERIFIER_CONTRACT_ADDRESS = \"$CONTRACT_ADDR\""
echo
echo "🚀 Then run:"
echo "   python watcher/watcher.py"
echo
echo "============================================================"
