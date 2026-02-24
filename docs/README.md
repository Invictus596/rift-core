# Rift Protocol Documentation

Welcome to the official Rift Protocol documentation!

## 📚 What is Rift Protocol?

**Rift Protocol** eliminates Bitcoin's 10-minute block latency by verifying the L1 mempool using ZK-proofs on Starknet in **under 2 seconds**.

> **Break the 10-Minute Barrier: Instant Bitcoin Verification on Starknet**

## 🎯 Quick Navigation

### New to Rift?
1. Start with [Technical Overview](docs/TECHNICAL_OVERVIEW.md)
2. Run the [2-Minute Demo](docs/HACKATHON_DEMO.md)
3. Read the [Architecture](docs/architecture.md)

### Developer?
1. Check [Getting Started](docs/getting_started.md)
2. Review [Tech Stack](docs/tech_stack.md)
3. Read [Contributing Guide](CONTRIBUTING.md)

### Judge/Reviewer?
1. [Technical Overview](docs/TECHNICAL_OVERVIEW.md) ⭐
2. [Demo Guide](docs/HACKATHON_DEMO.md)
3. [Evaluation Criteria](docs/TECHNICAL_OVERVIEW.md#-why-rift-protocol)

## 📖 Documentation Structure

```
📚 Rift Protocol Documentation
├── 🏠 Introduction
│   ├── Welcome to Rift Protocol
│   └── Technical Overview ⭐
├── 🚀 Getting Started
│   ├── Quick Start Guide
│   ├── Hackathon Demo
│   └── Installation
├── 📚 Core Documentation
│   ├── Architecture
│   ├── Tech Stack
│   └── Components
├── 🎓 Technical Deep Dive
│   ├── How It Works
│   ├── Cryptography
│   └── Smart Contracts
├── 📊 Project Status
│   ├── Completed Phases
│   └── Roadmap
├── 🔍 Use Cases
│   ├── Wrapped Runes
│   ├── Bitcoin NFTs
│   └── DeFi & Gaming
├── ⚠️ Technical Challenges
│   └── RPC Compatibility
├── 📖 Developer Guide
│   ├── Setup & Build
│   └── Contributing
└── 🎯 Hackathon Resources
    ├── For Judges
    └── Demo Resources
```

## 🎯 Key Documents

| Document | Description | Read Time |
|----------|-------------|-----------|
| [Technical Overview](docs/TECHNICAL_OVERVIEW.md) | Executive summary, architecture, presentation script | 5 min |
| [Hackathon Demo](docs/HACKATHON_DEMO.md) | Step-by-step demo guide | 3 min |
| [Architecture](docs/architecture.md) | System design and data flow | 10 min |
| [Getting Started](docs/getting_started.md) | Setup and deployment | 15 min |
| [RPC Issues](docs/RPC_ISSUES.md) | Technical challenge analysis | 5 min |
| [Phase 4 Plan](docs/PHASE4_EXECUTOR_PLAN.md) | Executor contract roadmap | 10 min |

## 🚀 Quick Start

### Run the Demo (2 Minutes)

```bash
# Clone and setup
git clone <your-repo-url>
cd rift-core-internal
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the demo
./watcher/run-hackathon-demo.sh
```

### Expected Output

```
========================================
  Rift Protocol - Hackathon Demo
========================================
[*] Starting Rift Watcher (MOCK_MODE: True)
[+] RIFT PROTOCOL TX DETECTED
    Transaction ID: 9a6c506b0685f13569be3e1e47b811998618f2cb...
    OP_RETURN Data: 1967b19fecd7335a986452494654df117e6edaaa...
--------------------------------------------------
```

## 🏗️ Architecture Overview

```
Bitcoin Mempool → Watcher (Python) → RPC Bridge → Verifier (Cairo) → Executor (L2)
                      ↓
                 Detects RIFT
                 transactions
```

### Core Components

| Component | Technology | Status |
|-----------|------------|--------|
| **Watcher** | Python | ✅ Complete |
| **Verifier** | Cairo 2.6.4 | ✅ Complete |
| **RPC Bridge** | starknet.py | ✅ Complete |
| **Executor** | Starknet | 📋 Planned |

## 💡 Use Cases

- **Wrapped Runes** - Instant minting on Starknet ($500M+ market)
- **Bitcoin NFTs** - Sub-second Ordinals trading ($1B+ market)
- **Bitcoin DEX** - Real-time Bitcoin DeFi ($50B+ market)
- **Cross-Chain Bridge** - Instant ZK-verified bridging ($10B+ market)
- **Bitcoin Gaming** - Real-time payments ($200B+ market)

## 📊 Project Status

**Current Phase: Phase 3** — RPC Bridge Complete

| Phase | Component | Status |
|-------|-----------|--------|
| Phase 1 | The Watcher | ✅ Completed |
| Phase 2 | The Verifier | ✅ Build Complete |
| Phase 3 | RPC Bridge | ✅ Complete |
| Phase 4 | The Executor | 📋 Planned |
| Phase 5 | Production Demo | 🎯 Next |

## 🔗 External Links

- **GitHub Repository**: [View on GitHub](https://github.com/your-repo)
- **Starknet**: [starknet.io](https://starknet.io/)
- **Cairo**: [cairo-lang.org](https://www.cairo-lang.org/)
- **Bitcoin**: [bitcoin.org](https://bitcoin.org/)

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**⚡ Making Bitcoin Instant**

[GitHub](https://github.com/your-repo) • [Documentation Index](SUMMARY.md) • [Technical Overview](docs/TECHNICAL_OVERVIEW.md)

</div>
