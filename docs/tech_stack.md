# 🛠️ Tech Stack & Resources

Rift is built using cutting-edge cryptography and cross-chain infrastructure.

## ⚡ Starknet (Layer 2)
The execution layer where verified Bitcoin transactions trigger state changes.

* **[Cairo v2](https://book.cairo-lang.org/):** The Turing-complete language for creating provable programs (STARKs) on Starknet.
* **[Garaga](https://github.com/keep-starknet-strange/garaga):** A high-efficiency Cairo library for pairing-based cryptography. We use Garaga to verify **Bitcoin secp256k1 signatures** directly inside the Starknet VM.
* **[Scarb](https://docs.swmansion.com/scarb/):** The Cairo package manager and build toolchain.
* **[Starkli](https://book.starkli.rs/):** Fast command-line tool for deploying and interacting with Starknet contracts.

## 🟠 Bitcoin (Layer 1)
The settlement and data availability layer.

* **[Bitcoin Testnet](https://en.bitcoin.it/wiki/Testnet):** We monitor the Bitcoin Testnet Mempool for "Rift-tagged" transactions (OP_RETURN).
* **[Bitcoin RPC](https://developer.bitcoin.org/reference/rpc/):** The standard JSON-RPC interface used by our Python Watcher to fetch raw transaction data.

## 🐍 Off-Chain Infrastructure
The "glue" that connects Bitcoin L1 to Starknet L2.

* **Python 3.10+:** The core logic for the **Watcher** service.
* **[Alchemy](https://www.alchemy.com/):** High-reliability RPC node provider for relaying transactions to Starknet Sepolia.
* **[GitHub Actions](https://github.com/features/actions):** (Planned) For CI/CD and automated testing of Cairo contracts.

## 📚 Key Documentation
* [Starknet Docs](https://docs.starknet.io/)
* [Cairo Book](https://book.cairo-lang.org/)
* [Garaga GitHub](https://github.com/keep-starknet-strange/garaga)
* [Bitcoin Developer Guide](https://developer.bitcoin.org/)
