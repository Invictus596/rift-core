# ⚡ Rift Protocol: Bitcoin L2 Execution Layer

> **Instant, Trustless Bitcoin Execution on Starknet.**

Rift eliminates Bitcoin's 10-minute block latency by verifying the L1 mempool using ZK-proofs on Starknet. It enables sub-second reaction times for Runes/Ordinals trading and gaming by proving the existence of unconfirmed Bitcoin transactions.

---

## 📋 Technical Overview

**New to Rift Protocol?** Start here → [Technical Overview Document](docs/TECHNICAL_OVERVIEW.md)

- ✅ **Live Demo**: `./watcher/run-hackathon-demo.sh`
- ✅ **2-Minute Presentation Script**: Included in overview
- ✅ **Technical Deep Dive**: Full architecture documented
- ✅ **Evaluation Criteria**: Project highlights addressed

---

## 🏗️ Architecture: Listen-Verify-Execute

| Component | Technology | Role |
|-----------|------------|------|
| **Watcher** | Python | Off-chain agent monitoring Bitcoin Mempool for `OP_RETURN` patterns |
| **Verifier** | Cairo 2.6.4 + Starknet Native | Smart contract verifying Bitcoin ECDSA/Schnorr signatures on-chain |
| **Executor** | Starknet | Triggers business logic on L2 instantly (e.g., minting Wrapped Runes) |

---

## 🚀 Project Status & Roadmap

We are currently in **Phase 3** — Python-to-Starknet RPC bridge complete. **Hackathon-ready in mock mode.**

| Phase | Component | Status | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | The Watcher | ✅ Completed | Python agent monitoring Bitcoin mempool, filtering OP_RETURN "RIFT" tags |
| **Phase 2** | The Verifier | ✅ Build Complete | Cairo 2.6.4 contract with interface-implementation pattern. Mock verification enabled for E2E testing. |
| **Phase 3** | RPC Bridge | ✅ Complete | Python-to-Starknet bridge using starknet.py. Watcher can now call Verifier contract on Katana/Starknet. |
| **Phase 4** | The Executor | 📋 Planned | L2 Contract to mint wrapped assets based on verified L1 events ([Plan](docs/PHASE4_EXECUTOR_PLAN.md)) |
| **Phase 5** | The Demo | 🎯 Hackathon Ready | Mock mode demonstration (full pipeline, simulated Starknet calls) |

> **Note**: On-chain deployment is blocked by RPC compatibility issues with both Sepolia (v0.10+) and Katana (v1.7.1). Both don't support the "pending" block tag that starkli 0.4.2 requires. See [docs/RPC_ISSUES.md](docs/RPC_ISSUES.md) for details. We demonstrate the full architecture in mock mode for the hackathon.

---

## 📂 Project Structure

```bash
rift-core-internal/
├── watcher/                    # Bitcoin mempool listener & Starknet RPC bridge
│   ├── watcher.py              # Main entry point (Mempool Poller)
│   ├── serializer.py           # Hex-to-Felt converter for Cairo
│   ├── rpc_bridge.py           # Starknet RPC communication (starknet.py)
│   ├── test_rpc_bridge.py      # Integration test for RPC bridge
│   └── README.md               # Watcher-specific documentation
├── contracts/                  # Cairo 2.6.4 contracts (Starknet)
│   ├── src/
│   │   ├── lib.cairo           # Module exports
│   │   └── verifier.cairo      # Verifier contract (IVerifier + VerifierImpl)
│   ├── Scarb.toml              # Dependencies (starknet 2.6.4, garaga v1.0.1)
│   └── target/                 # Build artifacts (Sierra, CASM)
├── docs/                       # Documentation
│   ├── architecture.md         # System architecture & data flow
│   ├── tech_stack.md           # Technology stack details
│   ├── contracts.md            # Deployed contract addresses
│   └── getting_started.md      # Setup & deployment guide
├── scripts/                    # Deployment & Integration scripts (coming soon)
├── requirements.txt            # Python dependencies (python-bitcoinrpc, starknet.py)
└── README.md                   # This file
```

---

## 🔧 Quick Start

### 🎯 Hackathon Demo (Recommended - 2 Minutes)

Due to persistent RPC compatibility issues with Sepolia and Katana (see [docs/RPC_ISSUES.md](docs/RPC_ISSUES.md)), we demonstrate the full pipeline in mock mode.

```bash
cd ~/rift-core-internal

# Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the hackathon demo
./watcher/run-hackathon-demo.sh
```

**What this demonstrates**:
- ✅ Bitcoin mempool monitoring
- ✅ RIFT tag detection in OP_RETURN data
- ✅ Transaction parsing and extraction
- ✅ RPC Bridge ready for Starknet integration

See [docs/HACKATHON_DEMO.md](docs/HACKATHON_DEMO.md) for full presentation guide.

---

### Prerequisites (Full Deployment)

```bash
# Install Scarb (Cairo toolchain)
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Install Starkli (Starknet CLI)
curl https://get.starkli.sh | sh
starkliup

# Install Katana (local Starknet node)
curl -L https://install.dojoengine.org | bash
dojoup install
```

---

### Build & Deploy Locally (When RPC Issues Resolved)

```bash
# 1. Start Katana (keep running in a separate terminal)
katana --validate-max-steps 4000000 --invoke-max-steps 4000000

# 2. Build the contract
cd contracts
scarb clean && scarb build

# 3. Test the RPC Bridge (deploys contract automatically)
cd ../watcher
python test_rpc_bridge.py

# Note the deployed contract address from the test output
```

### Run the Watcher

```bash
# Activate virtual environment
cd /home/invictus/rift-core-internal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the watcher (mock mode by default - no Starknet calls)
python watcher/watcher.py

# Enable Starknet integration (after deploying contract)
# Edit watcher/watcher.py:
#   STARKNET_RPC_MODE = True
#   VERIFIER_CONTRACT_ADDRESS = "0x..."  # From test_rpc_bridge.py output
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Hackathon Demo](docs/HACKATHON_DEMO.md) | 🎯 **Quick demo guide for hackathon presentations** |
| [RPC Issues](docs/RPC_ISSUES.md) | Technical details on Sepolia/Katana RPC compatibility problems |
| [Phase 4 Plan](docs/PHASE4_EXECUTOR_PLAN.md) | Complete Executor implementation roadmap |
| [Getting Started](docs/getting_started.md) | Setup guide for local development and deployment |
| [Architecture](docs/architecture.md) | System design, data flow, and contract details |
| [Tech Stack](docs/tech_stack.md) | Technology choices and dependencies |
| [Contracts](docs/contracts.md) | Deployed contract addresses |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **L1** | Bitcoin Testnet (mempool monitoring) |
| **L2** | Starknet 2.6.4 (Cairo 2023_11 edition) |
| **Crypto** | Starknet Native secp256k1 precompiles (Garaga v1.0.1 available) |
| **Off-chain** | Python 3.10+ (Watcher service) |
| **Dev Tools** | Scarb, Starkli, Katana |

---

## 🤝 Contributing

Contributions are welcome! Please read the documentation and open an issue to discuss major changes.

---

## 📄 License

MIT
