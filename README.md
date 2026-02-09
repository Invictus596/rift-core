# Rift: Bitcoin L2 Execution Layer

**Tagline:** Instant, Trustless Bitcoin Execution on Starknet.

Rift eliminates Bitcoin's 10-minute block latency by verifying the L1 mempool using ZK-proofs on Starknet. It enables sub-second reaction times for Runes/Ordinals trading and gaming by proving the existence of unconfirmed Bitcoin transactions.

## 🏗️ Architecture: Listen-Verify-Execute

**Watcher (Python/Rust):** A robust off-chain agent that monitors the Bitcoin Mempool. It filters for specific "Rift-compatible" transactions (e.g., specific OP_RETURN patterns).

**Verifier (Cairo + Garaga):** A Starknet smart contract that cryptographically verifies Bitcoin ECDSA/Schnorr signatures inside a ZK-STARK.

**Executor (Starknet):** Once verified, this contract triggers business logic on L2 instantly (e.g., minting a Wrapped Rune).

## 🚀 Project Status & Roadmap

We are currently building Phase 2.

| Phase | Component   | Status | Description |
|-------|-------------|--------|-------------|
| Phase 1 | The Watcher | ✅ Completed | Python agent to listen to Bitcoin Testnet mempool and filter for OP_RETURN "RIFT" tags. |
| Phase 2 | The Verifier | 🚧 WIP | (Current Focus) Cairo contracts using Garaga to verify Bitcoin signatures on Starknet. |
| Phase 3 | The Executor | ⏳ Planned | L2 Contract to mint assets based on verified L1 events. |
| Phase 4 | The Demo | ⏳ Planned | End-to-end "Snipe" demo: Broadcast L1 Tx -> L2 State Update < 2s. |

## 📂 Project Structure

```bash
rift-core/
├── watcher/           # Bitcoin mempool listener & data serializer
│   ├── watcher.py     # Main entry point (Mempool Poller)
│   └── serializer.py  # (WIP) Hex-to-Felt converter for Cairo
├── contracts/         # Cairo v2 contracts (Starknet)
│   └── src/           # Smart contract source code
├── scripts/           # Deployment & Integration scripts
└── requirements.txt   # Python dependencies
```

## 🛠️ Setup & Usage

### Prerequisites

- Python 3.10+
- Bitcoin Core node (optional, for Live Mode)
- Cairo / Scarb (for Phase 2+)

### Installation

```bash
git clone https://github.com/Invictus596/rift-core.git
cd rift-core
pip install -r requirements.txt
```

### Running the Watcher (Phase 1)

#### Option A: Mock Mode (Default)

Great for testing without a full node.

```bash
python3 watcher/watcher.py
# Output: Generating random mock transactions...
# [+] RIFT PROTOCOL TX DETECTED
```

#### Option B: Live Mode (Bitcoin Testnet)

1. Open `watcher/watcher.py` and set `MOCK_MODE = False`.
2. Update `RPC_USER`, `RPC_PASSWORD`, and `RPC_PORT`.
3. Run the script to listen to the real Testnet mempool.

## 📄 License

MIT

Built for the Starknet "Re{define}" Hackathon 2025.
