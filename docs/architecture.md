# 🏗️ Architecture

How Rift brings Bitcoin security to Starknet execution.

## The Flow
The Rift protocol consists of three main components working in a loop:

```mermaid
graph LR
    A[Bitcoin User] -- Broadcasts Tx --> B((Bitcoin Mempool))
    B -- "Contains OP_RETURN 'RIFT'" --> C[Watcher (Python)]
    C -- "Extracts Signature & Public Key" --> D{Verifier Contract}
    D -- "Verifies ECDSA/Schnorr" --> E[Executor Contract]
    E -- "Mints Assets" --> F[Starknet User]
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
```

### Components
1. **The Watcher:** A Python-based agent that listens to the Bitcoin P2P network.
2. **The Verifier:** A Cairo smart contract using **Garaga** to verify Bitcoin signatures inside a ZK-proof.
3. **The Executor:** The L2 contract that mints assets based on verified events.
