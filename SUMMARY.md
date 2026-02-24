# Table of Contents

## 🏠 Introduction
* [Welcome to Rift Protocol](README.md)
* [📖 Technical Overview](docs/TECHNICAL_OVERVIEW.md) ⭐ **Start Here**

## 🚀 Getting Started
* [Quick Start Guide](docs/getting_started.md)
* [🎯 Hackathon Demo](docs/HACKATHON_DEMO.md)
* [🔧 Quick Start (README)](README.md#-quick-start-demo)

## 📚 Core Documentation

### Architecture & Design
* [🏗️ System Architecture](docs/architecture.md)
* [🛠️ Technology Stack](docs/tech_stack.md)
* [📦 Project Structure](README.md#-project-structure)

### Components
* [👁️ Rift Watcher](watcher/README.md)
  * [Watcher Implementation](watcher/watcher.py)
  * [RPC Bridge](watcher/rpc_bridge.py)
  * [Serializer](watcher/serializer.py)
* [🔐 Verifier Contract](contracts/src/verifier.cairo)

## 🎓 Technical Deep Dive

### How It Works
* [Listen → Verify → Execute](docs/architecture.md)
* [Bitcoin Mempool Monitoring](watcher/README.md#mempool-monitoring)
* [RIFT Tag Detection](watcher/README.md#rift-tag-detection)
* [Starknet RPC Bridge](watcher/rpc_bridge.py)

### Cryptography
* [secp256k1 Verification](docs/tech_stack.md)
* [Starknet Native Precompiles](docs/tech_stack.md#crypto-layer)
* [Garaga Library](docs/tech_stack.md)

## 📊 Project Status

### Completed Phases
* [✅ Phase 1: The Watcher](README.md#-project-status--roadmap)
* [✅ Phase 2: The Verifier](README.md#-project-status--roadmap)
* [✅ Phase 3: RPC Bridge](README.md#-project-status--roadmap)

### Planned Phases
* [📋 Phase 4: The Executor](docs/PHASE4_EXECUTOR_PLAN.md)
* [🎯 Phase 5: Production Demo](README.md#-project-status--roadmap)

## 🔍 Use Cases

### Market Opportunities
* [💰 Wrapped Runes](README.md#-use-cases)
* [🎨 Bitcoin NFTs](README.md#-use-cases)
* [📈 Bitcoin DEX](README.md#-use-cases)
* [🌉 Cross-Chain Bridge](README.md#-use-cases)
* [🎮 Bitcoin Gaming](README.md#-use-cases)

## ⚠️ Technical Challenges

### RPC Compatibility Issues
* [Problem Overview](docs/RPC_ISSUES.md)
* [Sepolia RPC v0.10+ Issue](docs/RPC_ISSUES.md#issue-1-alchemy-sepolia-rpc-v010)
* [Katana v1.7.1 Issue](docs/RPC_ISSUES.md#issue-2-katana-local-node)
* [Workarounds](docs/RPC_ISSUES.md#workarounds)
* [Mock Mode](docs/HACKATHON_DEMO.md)

## 📖 Developer Guide

### Setup & Installation
* [Prerequisites](docs/getting_started.md#prerequisites)
* [Installation Steps](docs/getting_started.md#installation)
* [Environment Configuration](docs/getting_started.md#configuration)

### Building & Testing
* [Build Contracts](docs/getting_started.md#building-contracts)
* [Run Tests](docs/getting_started.md#testing)
* [Deploy Locally](docs/getting_started.md#local-deployment)

### Contributing
* [Contribution Guidelines](CONTRIBUTING.md)
* [Code Style](CONTRIBUTING.md#code-style)
* [Pull Request Process](CONTRIBUTING.md#pull-requests)

## 🎯 Hackathon Resources

### For Judges & Reviewers
* [Evaluation Criteria](docs/TECHNICAL_OVERVIEW.md#-why-rift-protocol)
* [2-Minute Presentation Script](docs/TECHNICAL_OVERVIEW.md#-presentation-script-2-minutes)
* [Demo Instructions](docs/HACKATHON_DEMO.md)
* [Submission Checklist](SUBMISSION_CHECKLIST.md)
* [Submission Summary](SUBMISSION_SUMMARY.md)

### Demo Resources
* [Run Demo (2 min)](docs/HACKATHON_DEMO.md#-quick-start-5-minutes)
* [Expected Output](README.md#-run-the-hackathon-demo-2-minutes)
* [Demo Metrics](docs/HACKATHON_DEMO.md#-demo-metrics)
* [Troubleshooting](docs/HACKATHON_DEMO.md#-troubleshooting)

## 📁 Project Structure

```
rift-core-internal/
├── watcher/              # Bitcoin mempool listener
├── contracts/            # Cairo smart contracts
├── docs/                 # Documentation
├── scripts/              # Deployment scripts
├── README.md             # Main overview
├── CONTRIBUTING.md       # Contribution guide
└── SUMMARY.md            # This file (GitBook TOC)
```

## 🔗 External Resources

### Official Documentation
* [Starknet Docs](https://docs.starknet.io/)
* [Cairo Docs](https://book.cairo-lang.org/)
* [Bitcoin Wiki](https://en.bitcoin.it/wiki/Main_Page)

### Tools & Libraries
* [Scarb (Cairo Package Manager)](https://docs.swmansion.com/scarb/)
* [Starkli (Starknet CLI)](https://github.com/foundry-rs/starkli)
* [starknet.py](https://starknetpy.readthedocs.io/)
* [Garaga (Cairo Crypto)](https://github.com/keep-starknet-strange/garaga)

## 📞 Community & Support

### Get Help
* [Report an Issue](https://github.com/your-repo/issues)
* [Request a Feature](https://github.com/your-repo/issues)
* [Contributing Guide](CONTRIBUTING.md)

### Contact
* [GitHub Repository](https://github.com/your-repo)
* [Documentation Index](README.md#-documentation)

---

## 📊 Quick Reference

| Topic | Document | Time |
|-------|----------|------|
| **What is Rift?** | [Technical Overview](docs/TECHNICAL_OVERVIEW.md) | 5 min |
| **Run Demo** | [Hackathon Demo](docs/HACKATHON_DEMO.md) | 2 min |
| **Architecture** | [System Architecture](docs/architecture.md) | 10 min |
| **Setup Dev Env** | [Getting Started](docs/getting_started.md) | 15 min |
| **RPC Issues** | [RPC Problems](docs/RPC_ISSUES.md) | 5 min |
| **Phase 4 Plan** | [Executor Plan](docs/PHASE4_EXECUTOR_PLAN.md) | 10 min |

---

<div align="center">

**⚡ Rift Protocol: Making Bitcoin Instant**

[Back to Top](#table-of-contents) • [GitHub](https://github.com/your-repo) • [Technical Overview](docs/TECHNICAL_OVERVIEW.md)

</div>
