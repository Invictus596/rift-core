# 🏗️ Architecture

How Rift brings Bitcoin security to Starknet execution.

---

## 🔄 The Execution Flow

Rift eliminates latency by creating a "Fast Lane" for Bitcoin transactions.

> **1. 📡 User Broadcasts**
> A Bitcoin user sends a transaction with the `OP_RETURN "RIFT"` tag.
>
> ⬇️ *0 Seconds (Mempool)*
>
> **2. 🕵️ Watcher Detects**
> The Python Watcher spots the unconfirmed transaction, extracts the **Signature** and **Public Key**.
>
> ⬇️ *Relayed to Starknet*
>
> **3. ⚖️ Verifier Proves**
> The **Rift Verifier** (Cairo contract) uses **Garaga** to cryptographically verify the Bitcoin signature on-chain.
>
> ⬇️ *Sub-Second Execution*
>
> **4. ⚡ Executor Mints**
> Once verified, the **Executor Contract** instantly mints the Wrapped Rune or updates the game state.

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
