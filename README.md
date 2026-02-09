# Rift - Bitcoin L2 Execution Layer

Rift eliminates Bitcoin's 10-minute block latency by verifying the L1 mempool using ZK-proofs on Starknet.

## Project Structure

```
rift-core/
├── watcher/           # Bitcoin mempool watcher
│   └── watcher.py     # Main watcher script
├── contracts/         # Cairo contracts for Starknet
├── scripts/           # Utility scripts
└── requirements.txt   # Python dependencies
```

## Setup

### Prerequisites

- Python 3.8+
- Bitcoin Core node (for real mode) or use MOCK_MODE for testing

### Installation

1. Clone the repository
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### Running the Watcher

#### Mock Mode (Default)
For testing without a Bitcoin node:

```bash
cd watcher
python watcher.py
```

The script will generate random mock transactions and detect those containing the "RIFT" tag.

#### Real Mode
To connect to a Bitcoin Testnet node:

1. Update the RPC credentials in `watcher.py`
2. Set `MOCK_MODE = False`
3. Run the script:

```bash
cd watcher
python watcher.py
```

## Mechanism: Listen-Verify-Execute

- **Watcher**: Listens to Bitcoin Mempool for specific transactions
- **Verifier**: Cryptographically verifies the Bitcoin signature/transaction on Starknet
- **Executor**: Updates L2 state instantly upon verification

## Current Status: Phase 1 - The Watcher

The watcher polls the Bitcoin mempool every 2 seconds looking for transactions with an OP_RETURN output containing the hex tag `52494654` (which spells "RIFT").
