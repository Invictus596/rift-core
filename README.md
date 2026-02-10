# Rift: Bitcoin L2 Execution Layer

> **Instant, Trustless Bitcoin Execution on Starknet.**

Rift eliminates Bitcoin's 10-minute block latency by verifying the L1 mempool using ZK-proofs on Starknet. It enables sub-second reaction times for Runes/Ordinals trading and gaming by proving the existence of unconfirmed Bitcoin transactions.

---

## 🏗️ Architecture: Listen-Verify-Execute

* **Watcher (Python/Rust):** A robust off-chain agent that monitors the Bitcoin Mempool. It filters for specific "Rift-compatible" transactions (e.g., specific `OP_RETURN` patterns).
* **Verifier (Cairo + Garaga):** A Starknet smart contract powered by **Garaga** (the efficient pairing library). It cryptographically verifies Bitcoin ECDSA/Schnorr signatures and ZK-STARK proofs directly on-chain, allowing for trustless state updates from the Watcher.
* **Executor (Starknet):** Once verified, this contract triggers business logic on L2 instantly (e.g., minting a Wrapped Rune).

## 🚀 Project Status & Roadmap

We are currently building **Phase 2**.

| Phase | Component | Status | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | The Watcher | ✅ Completed | Python agent to listen to Bitcoin Testnet mempool and filter for OP_RETURN "RIFT" tags. |
| **Phase 2** | The Verifier | 🏗️ In Progress | Integrating **Garaga** for signature verification. Deploying `rift_verifier.cairo` to Starknet Sepolia. |
| **Phase 3** | The Executor | ⏳ Planned | L2 Contract to mint assets based on verified L1 events. |
| **Phase 4** | The Demo | ⏳ Planned | End-to-end "Snipe" demo: Broadcast L1 Tx -> L2 State Update < 2s. |

## 📂 Project Structure

```bash
rift-core/
├── watcher/           # Bitcoin mempool listener & data serializer
│   ├── watcher.py     # Main entry point (Mempool Poller)
│   └── serializer.py  # (WIP) Hex-to-Felt converter for Cairo
├── contracts/         # Cairo v2 contracts (Starknet)
│   ├── src/
│   │   ├── lib.cairo           # Contract interface
│   │   └── rift_verifier.cairo # Main Verifier logic (Garaga integration)
│   └── Scarb.toml     # Dependencies (includes Garaga)
├── scripts/           # Deployment & Integration scripts
└── requirements.txt   # Python dependencies (includes garaga-py)