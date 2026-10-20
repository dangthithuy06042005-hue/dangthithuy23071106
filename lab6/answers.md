# Lab 06 Submission — ClassRegistry on Hardhat + TrustKeys

- **Student Name:** Dang Thi Thuy
- **Deployer Wallet Address:** `0x34A07f3a288720977823A6694280620Afb60ec63`
- **ClassRegistry Contract Address (TrustKeys Testnet):** `0xe7dc51A8AdbB430aE18110818A39CdCBc571C130`
- **Register Transaction Hash:** `0xbb6fac2db4e4191e7371f04b00584f56cf97ce06abfd2fc532d941d4dc76e909`
- **Confirmed Block Number:** `718058`

---

## Answers to Lab Questions (Q1 — Q5)

### Q1: Where did the sample test run — on TrustKeys or a local chain? What did it cost in gas?
- **Where it ran:** The sample test ran on the **local in-memory Hardhat Network** hosted entirely within the computer's RAM, completely independent from TrustKeys or any public blockchain network.
- **Gas cost:** It cost **$0** (zero real funds). The test consumed virtual/mock test ETH pre-funded within Hardhat's ephemeral local test environment.

### Q2: Why is `register(string calldata name)` cheaper than `string memory name`?
- **Reason:** `calldata` is a non-modifiable, **read-only** data location that points directly to the incoming transaction's input payload.
- In contrast, using `string memory name` requires the EVM to allocate a new memory segment and copy all bytes from `calldata` into `memory`, which consumes additional opcodes and incurs memory expansion gas costs. Using `calldata` bypasses this copy step, resulting in significant gas savings.

### Q3: Why keep a separate `address[]` when the `mapping` already stores names?
- **Reason:** In Solidity, a `mapping` is an internal hash table. It does not store keys and does not possess a `.length` property, making it **impossible to iterate over or retrieve a list of all keys**.
- Maintaining a dedicated `address[] members` array is necessary to:
  1. Enumerate and return the total count of registered members via `members.length`.
  2. Enable sequential iteration and indexing over all registered members (`memberAt(index)`).

### Q4: Deploying is a transaction — who paid the gas, and in which coin?
- **Who paid the gas:** The deployer account (`0x34A07f3a288720977823A6694280620Afb60ec63`) whose private key was configured in the `.env` file to sign and broadcast the deployment transaction.
- **Coin used:** It was paid in the native currency (native token) of the **TrustKeys L1 Testnet** (`TRUST`).

### Q5: `queryFilter` reads the event log. How would a website use this to show a live member list?
- A Web3 frontend application would combine two techniques:
  1. **Initial Load (Historical Sync):** When the webpage loads, it calls `contract.queryFilter(contract.filters.Registered())` to fetch all past `Registered` events emitted from block 0 to the latest block, reconstructing the full member list.
  2. **Live Updates (Real-time Listening):** It registers an event listener via `contract.on("Registered", (who, name) => { ... })` over a WebSocket/RPC provider. Whenever a new registration transaction confirms on-chain, the listener fires immediately and dynamically appends the new member to the user interface without requiring a page refresh.
