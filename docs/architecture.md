# 🏗️ Architecture

How Rift brings Bitcoin security to Starknet execution.

---

## 🔄 The Execution Flow

Rift eliminates latency by creating a "Fast Lane" for Bitcoin transactions.

<div align="center">

```mermaid
graph TD
    %% Styling
    classDef core fill:#2c3e50,stroke:#34495e,stroke-width:2px,color:white;
    classDef btc fill:#f7931a,stroke:#d35400,stroke-width:2px,color:white;
    classDef stark fill:#3b3c97,stroke:#2c3e50,stroke-width:2px,color:white;

    %% Nodes
    User((Bitcoin User)):::btc
    Mempool[Bitcoin Mempool]:::btc
    Watcher(Rift Watcher):::core
    Verifier{Verifier Contract}:::stark
    Executor[Executor Contract]:::stark
    L2User((Starknet User)):::stark

    %% Flow (Vertical)
    User -->|Broadcasts Tx| Mempool
    Mempool -->|1. Detects OP_RETURN| Watcher
    Watcher -->|2. Sends Sig + Key| Verifier
    Verifier -->|3. ZK-Verify Sig| Executor
    Executor -->|4. Mint Assets| L2User
```

</div>

*(Figure 1: The Watcher listens to the Mempool, extracts the signature, and proves validity on Starknet in sub-seconds.)*

---

## 🧩 Protocol Components

### 1. The Watcher (Python)
An off-chain agent that scans the Bitcoin Mempool.
* **Role:** Detective 🕵️
* **Action:** Finds transactions with the `OP_RETURN "RIFT"` tag.
* **Output:** Extracts the `public_key` and `signature` and sends them to Starknet.

### 2. The Verifier (Cairo Contract)
The security heart of the protocol.
* **Role:** Judge ⚖️
* **Tech:** Uses **Garaga** to verify cryptographic signatures (secp256k1).
* **Verdict:** If the signature is valid, it approves the transaction immediately.

### 3. The Executor (L2 Contract)
The business logic layer.
* **Role:** Builder 🏗️
* **Action:** Mints assets, updates game state, or triggers DeFi swaps instantly.
