# 🛠️ Tech Stack & Resources

Rift is built using cutting-edge cryptography and cross-chain infrastructure.

---

## ⚡ Starknet (Layer 2)

The execution layer where verified Bitcoin transactions trigger state changes.

| Component | Version | Purpose |
|-----------|---------|---------|
| **Starknet** | 2.6.4 | Layer 2 rollup for ZK-proof execution |
| **Cairo** | 2.6.4 (2023_11 edition) | Turing-complete language for provable programs (STARKs) |
| **Scarb** | Latest | Cairo package manager and build toolchain |
| **Starkli** | Latest | CLI tool for deploying and interacting with Starknet contracts |
| **Katana** | Latest | Local Starknet development node for testing |

### Cairo 2.6.4 Migration

> **Note:** Rift has been migrated to **Cairo 2.6.4** using the **2023_11 edition**. This migration includes:
> - Modern interface-implementation pattern (`#[starknet::interface]` + `#[abi(embed_v0)]`)
> - Updated storage access syntax (`.read()` and `.write()` on storage pointers)
> - New event system with `#[event]` and `#[derive(starknet::Event)]`
> - Improved type safety and compiler diagnostics

### Cryptographic Libraries

| Library | Status | Purpose |
|---------|--------|---------|
| **Garaga** | ✅ Integrated (v1.0.1) | High-efficiency Cairo library for pairing-based cryptography |
| **Starknet Native Precompiles** | 🏗️ Priority | Native secp256k1 syscalls for gas-efficient signature verification |

> **Garaga Integration Note:** Garaga is included as a dependency in `Scarb.toml`. However, we are currently prioritizing **Starknet's native secp256k1 precompiles** for signature verification due to:
> - Lower gas costs
> - Better compatibility with Starknet 2.6.4
> - Simpler integration path for Phase 2 deployment
>
> Garaga may be utilized in future phases for advanced pairing operations or custom curve support.

---

## 🟠 Bitcoin (Layer 1)

The settlement and data availability layer.

| Component | Version | Purpose |
|-----------|---------|---------|
| **Bitcoin Testnet** | Latest | Monitor mempool for "Rift-tagged" transactions (OP_RETURN) |
| **Bitcoin RPC** | JSON-RPC 2.0 | Standard interface for fetching raw transaction data |

### Python Dependencies

```txt
python-bitcoinrpc==1.0
requests==2.31.0
```

---

## 🐍 Off-Chain Infrastructure

The "glue" that connects Bitcoin L1 to Starknet L2.

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.10+ | Core logic for the **Watcher** service |
| **Alchemy** | Latest | High-reliability RPC provider for Starknet Sepolia |
| **GitHub Actions** | ⏳ Planned | CI/CD and automated testing of Cairo contracts |

---

## 📚 Key Documentation

| Resource | Link |
|----------|------|
| Starknet Docs | https://docs.starknet.io/ |
| Cairo Book | https://book.cairo-lang.org/ |
| Scarb Docs | https://docs.swmansion.com/scarb/ |
| Starkli Book | https://book.starkli.rs/ |
| Garaga GitHub | https://github.com/keep-starknet-strange/garaga |
| Bitcoin Developer Guide | https://developer.bitcoin.org/ |
| Dojo Engine (Katana) | https://book.dojoengine.org/ |
