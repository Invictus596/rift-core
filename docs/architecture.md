# 🏗️ Architecture

How Rift brings Bitcoin security to Starknet execution.

---

## 🔄 The Execution Flow

Rift eliminates latency by creating a "Fast Lane" for Bitcoin transactions.

![Rift Architecture Diagram](https://mermaid.ink/img/pako:eNpVkM1qwzAQhF9F7NTA-QIOhV5KITSXQC8l1tpayVbyR7YRjO-e1U5KAz0sM_vN7K5QW80oI-z1c_PAa-a84a_n54HjR7bjl_rTz5OfL-fH2_v19fP69vnx_Xw5Pdx_vN2_fT9s-wdqf9QWqB-oQzSj8uCFyqH2kLw2aK_QIO6c9vYI9Z0Gq3v0iK5DcxO0c9AG7R2aO43-_8kR3Y46dLS_oF_R7dAv6H6hX9E9Qv-Ffmc_sF-4L-w_NoxYI2Y8IkZMOCJmPCLW7FhxzY4V1-xYcc2OFdfsWHHNjhV37Fhxx44Vd-xYcc_O_wLqdx8A)

*(Diagram: The Watcher listens to the Mempool, extracts the signature, and sends it to the Starknet Verifier for instant settlement.)*

---

## 🧩 Protocol Components

> **💡 The Core Innovation**
> Most bridges wait for 6 blocks (60 mins). Rift verifies the **Signature** in the mempool (0 seconds), using ZK-proofs to handle the risk.

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
