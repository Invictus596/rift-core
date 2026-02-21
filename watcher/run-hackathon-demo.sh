#!/bin/bash
# Rift Protocol - Hackathon Demo Script (Mock Mode)
# 
# This script runs the Rift Watcher in mock mode for hackathon demonstrations.
# Due to persistent RPC compatibility issues with both Sepolia and Katana,
# we demonstrate the full pipeline using mock transactions.
#
# Usage: ./run-hackathon-demo.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "  Rift Protocol - Hackathon Demo"
echo "  Mock Mode Demonstration"
echo "========================================"
echo ""

# Check Python virtual environment
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "[*] Creating Python virtual environment..."
    cd "$PROJECT_ROOT"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "[*] Activating Python virtual environment..."
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

echo ""
echo "Configuration:"
echo "  - Mode: MOCK (simulated Bitcoin transactions)"
echo "  - RIFT Tag: 52494654 (hex for 'RIFT')"
echo "  - Poll Interval: 2 seconds"
echo "  - Duration: 20 polling cycles (~40 seconds)"
echo ""
echo "What this demonstrates:"
echo "  ✅ Bitcoin mempool monitoring"
echo "  ✅ RIFT tag detection in OP_RETURN data"
echo "  ✅ Transaction parsing and extraction"
echo "  ✅ RPC Bridge ready for Starknet integration"
echo ""
echo "Note: Starknet RPC integration is disabled due to"
echo "      compatibility issues (see docs/RPC_ISSUES.md)"
echo ""
echo "Starting watcher..."
echo "----------------------------------------"

cd "$PROJECT_ROOT"
python watcher/watcher.py

echo ""
echo "========================================"
echo "  Demo Complete!"
echo "========================================"
echo ""
echo "Next Steps for Production:"
echo "  1. Resolve RPC compatibility issues"
echo "  2. Deploy Verifier contract to Starknet"
echo "  3. Set STARKNET_RPC_MODE=True in watcher.py"
echo "  4. Update VERIFIER_CONTRACT_ADDRESS"
echo ""
