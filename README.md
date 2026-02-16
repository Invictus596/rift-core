# Rift: Bitcoin L2 Execution Layer

> **Instant, Trustless Bitcoin Execution on Starknet.**

Rift eliminates Bitcoin's 10-minute block latency by verifying the L1 mempool using ZK-proofs on Starknet. It enables sub-second reaction times for Runes/Ordinals trading and gaming by proving the existence of unconfirmed Bitcoin transactions.

---

## 🏗️ Architecture: Listen-Verify-Execute

| Component | Technology | Role |
|-----------|------------|------|
| **Watcher** | Python | Off-chain agent monitoring Bitcoin Mempool for `OP_RETURN` patterns |
| **Verifier** | Cairo 2.6.4 + Starknet Native | Smart contract verifying Bitcoin ECDSA/Schnorr signatures on-chain |
| **Executor** | Starknet | Triggers business logic on L2 instantly (e.g., minting Wrapped Runes) |

---

## 🚀 Project Status & Roadmap

We are currently in **Phase 2** — Verifier contract built and ready for deployment.

| Phase | Component | Status | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | The Watcher | ✅ Completed | Python agent listening to Bitcoin Testnet mempool, filtering OP_RETURN "RIFT" tags |
| **Phase 2** | The Verifier | 🏗️ Build Complete / Deploying | Cairo 2.6.4 contract with interface-implementation pattern. Mock verification enabled for E2E testing. Native secp256k1 precompiles being integrated. |
| **Phase 3** | The Executor | ⏳ Planned | L2 Contract to mint assets based on verified L1 events |
| **Phase 4** | The Demo | ⏳ Planned | End-to-end "Snipe" demo: Broadcast L1 Tx → L2 State Update < 2s |

---

## 📂 Project Structure

```bash
rift-core-internal/
├── watcher/                    # Bitcoin mempool listener & data serializer
│   ├── watcher.py              # Main entry point (Mempool Poller)
│   └── serializer.py           # Hex-to-Felt converter for Cairo
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
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Quick Start

### Prerequisites

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

### Build & Deploy Locally

```bash
# 1. Start Katana (keep running)
katana --validate

# 2. Build the contract
cd contracts
scarb clean && scarb build

# 3. Declare to Katana
starkli --network http://localhost:5050 \
  declare ./target/dev/rift_verifier_Verifier.contract_class.json

# 4. Deploy the contract
starkli --network http://localhost:5050 \
  deploy <CLASS_HASH> <OWNER_ADDRESS>
```

### Run the Watcher

```bash
# Activate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the watcher (mock mode by default)
python3 watcher/watcher.py
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
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
