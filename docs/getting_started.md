# 🚀 Getting Started

Follow this guide to set up the **Rift Protocol** environment on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

* **[Python 3.10+](https://www.python.org/downloads/)**: Required for the Watcher agent.
* **[Scarb](https://docs.swmansion.com/scarb/download)**: The Cairo package manager (for building contracts).
* **[Starkli](https://book.starkli.rs/getting-started/installation)**: The CLI tool for deploying to Starknet.
* **[Git](https://git-scm.com/downloads)**: To clone the repository.

---

## 📥 Installation

### 1. Clone the Repository
Get the latest version of the Rift codebase.

```bash
git clone https://github.com/Invictus596/rift-core.git
cd rift-core
```

### 2. Install Python Dependencies
We recommend using a virtual environment (venv) to keep your system clean.

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

---

## ⚙️ Configuration

The Watcher needs to connect to a Bitcoin Node (or use Mock Mode) and a Starknet RPC.

### Option A: Mock Mode (Easiest)
By default, the Watcher runs in **Mock Mode**. It generates fake Bitcoin transactions to test the Starknet flow without needing a 500GB Bitcoin node.

* **No configuration required.** Just run the watcher!

### Option B: Live Mode (Testnet)
To listen to real Bitcoin Testnet transactions:

1. Open `watcher/watcher.py`.
2. Set `MOCK_MODE = False`.
3. Update the RPC credentials:
   ```python
   RPC_USER = "your_user"
   RPC_PASS = "your_password"
   RPC_PORT = 18332  # Standard Testnet Port
   ```

---

## 🏃‍♂️ Running the Protocol

### 1. Start the Watcher
This will start polling for `OP_RETURN` transactions.

```bash
python3 watcher/watcher.py
```

> **Output:**
> `[+] RIFT PROTOCOL TX DETECTED`
> `[i] Signature extracted...`
> `[>] Relaying to Starknet Verifier...`

### 2. Deploy Contracts (Phase 2)
If you are developing the smart contracts:

```bash
cd contracts
scarb build
starkli declare target/dev/rift_verifier.sierra.json
```
