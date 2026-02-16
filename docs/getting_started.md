# 🚀 Getting Started

Follow this guide to set up the **Rift Protocol** environment on your local machine.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.10+ | Required for the Watcher agent |
| **Scarb** | Latest | Cairo package manager (build contracts) |
| **Starkli** | Latest | CLI for deploying to Starknet |
| **Katana** | Latest | Local Starknet development node |
| **Git** | Latest | Clone the repository |

### Install Prerequisites

```bash
# Install Scarb (Cairo toolchain)
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Install Starkli (Starknet CLI)
curl https://get.starkli.sh | sh
starkliup

# Install Dojo Engine (includes Katana)
curl -L https://install.dojoengine.org | bash
dojoup install
```

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

### Bitcoin Node Configuration

The Watcher needs to connect to a Bitcoin Node (or use Mock Mode) and a Starknet RPC.

#### Option A: Mock Mode (Easiest)

By default, the Watcher runs in **Mock Mode**. It generates fake Bitcoin transactions to test the Starknet flow without needing a 500GB Bitcoin node.

- **No configuration required.** Just run the watcher!

#### Option B: Live Mode (Testnet)

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

## 🏠 Local Development with Katana

For local testing and development, use **Katana** — a fast, local Starknet development node.

### Step 1: Start Katana

```bash
# Start Katana with default configuration
katana --validate
```

**Expected Output:**
```
🔨 Starting Katana v0.x.x
📡 RPC server started on: http://127.0.0.1:5050
💰 Pre-funded accounts:
  | Account address | 0x05f94... |
  | Private key     | 0x1234...  |
  | Public key      | 0x5678...  |
```

> **Note:** Keep this terminal open — Katana must stay running for local development.

### Step 2: Create Account Configuration

Create a `katana-account.json` file to interact with the local node:

```bash
# Create account config (replace with Katana's pre-funded account details)
cat > katana-account.json << EOF
{
  "version": 1,
  "variant": {
    "type": "open_zeppelin",
    "version": 1,
    "public_key": "<PUBLIC_KEY_FROM_KATANA_OUTPUT>"
  },
  "deployment": {
    "status": "deployed",
    "class_hash": "<CLASS_HASH>",
    "address": "<ACCOUNT_ADDRESS>"
  }
}
EOF
```

### Step 3: Build the Contract

```bash
cd contracts

# Clean previous build artifacts
scarb clean

# Build the contract (downloads dependencies)
scarb build
```

**Expected Output:**
```
   Compiling rift_verifier v0.1.0 (...)
    Finished release target(s) in XX seconds
```

### Step 4: Declare the Contract

Upload the contract class to Katana:

```bash
starkli --network http://localhost:5050 \
  --account katana-account.json \
  declare ./target/dev/rift_verifier_Verifier.contract_class.json
```

**Copy the `CLASS_HASH` from the output.**

### Step 5: Deploy the Contract

Deploy an instance of the contract:

```bash
# Replace <CLASS_HASH> with the actual class hash from Step 4
# Replace <OWNER_ADDRESS> with your account address
starkli --network http://localhost:5050 \
  --account katana-account.json \
  deploy <CLASS_HASH> <OWNER_ADDRESS>
```

**Copy the `CONTRACT_ADDRESS` from the output.**

### Step 6: Interact with the Contract

```bash
# Check verification count
starkli --network http://localhost:5050 \
  call <CONTRACT_ADDRESS> get_verification_count

# Check if a transaction is verified
starkli --network http://localhost:5050 \
  call <CONTRACT_ADDRESS> is_verified 0x1234...

# Get contract owner
starkli --network http://localhost:5050 \
  call <CONTRACT_ADDRESS> get_owner
```

---

## 🏃‍♂️ Running the Protocol

### 1. Start the Watcher

This will start polling for `OP_RETURN` transactions.

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the watcher
python3 watcher/watcher.py
```

> **Output:**
> ```
> [*] Starting Rift Watcher (MOCK_MODE: True)
> [*] Looking for transactions with OP_RETURN containing hex tag: 52494654 ('RIFT')
> [*] Starting mempool monitoring...
> [+] RIFT PROTOCOL TX DETECTED
>     Transaction ID: abc123...
>     Raw Hex Data: 02000000...
>     OP_RETURN Data: ...
> ```

### 2. Deploy Contracts (Phase 2)

For local development, follow the **Local Development with Katana** section above.

For testnet deployment:

```bash
cd contracts

# Build the contract
scarb build

# Declare to Starknet Sepolia
starkli --network sepolia \
  --account ~/.starkli-wallets/<your-account>/account.json \
  declare ./target/dev/rift_verifier_Verifier.contract_class.json

# Deploy the contract
starkli --network sepolia \
  --account ~/.starkli-wallets/<your-account>/account.json \
  deploy <CLASS_HASH> <OWNER_ADDRESS>
```

---

## 📝 Next Steps

1. **Update Contract Addresses:** After deployment, update `docs/contracts.md` with your deployed addresses.
2. **Connect Watcher to Contract:** Modify `watcher/watcher.py` to call the deployed contract using Starknet RPC.
3. **Test End-to-End:** Run the watcher and verify transactions are recorded on-chain.
4. **Implement Crypto Verification:** Replace mock verification with native secp256k1 precompiles.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `scarb build` fails | Ensure you have the latest Scarb version and Cairo 2.6.4 toolchain |
| Katana won't start | Check if port 5050 is available; try `katana --port 5051` |
| Starkli declaration fails | Ensure your account is funded with test tokens |
| Contract interaction fails | Verify the contract address and network URL are correct |

---

## 📚 Additional Resources

- [Starknet Documentation](https://docs.starknet.io/)
- [Cairo Book](https://book.cairo-lang.org/)
- [Starkli Book](https://book.starkli.rs/)
- [Katana Documentation](https://book.dojoengine.org/toolchain/katana.html)
