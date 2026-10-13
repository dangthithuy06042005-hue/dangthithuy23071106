# Lab 04 Answers (Detailed Explanations)

**Q1: The target has roughly how many leading zero hex digits? How many bits of work does one valid header represent (~2^?)?**

**Answer:**
- **Leading Zero Hex Digits:** If you look at the computed target (`000000000000000000034219...`), you can count exactly **19 leading zeros** before the first non-zero digit (`3`).
- **Bits of Work:**
  - Every hexadecimal digit represents 4 bits in binary (e.g., `0` in hex is `0000` in binary). 
  - 19 hex zeros equals $19 \times 4 = 76$ leading zero bits.
  - The next hex digit is `3`, which is `0011` in binary. This gives us **2 additional leading zero bits**.
  - Therefore, a valid hash must have at least **78 leading zero bits** in total (76 + 2).
- **Conclusion:** Because the chance of getting a `0` bit by random guessing is 50% (or 1/2), getting 78 zeros in a row requires, on average, $2^{78}$ random guesses. Thus, one valid header mathematically proves that the network performed roughly **~2^78 to 2^79** hash operations (bits of work) to find it.

---

**Q2: Verifying the PoW took your laptop 2 hash calls. Finding it took the network ~10 minutes at ~102 H/s. What property of SHA-256 creates this asymmetry?**

**Answer:**
- This massive asymmetry (hard to find, easy to verify) is created by the **One-Way Function** property of cryptographic hashes, specifically **Pre-image Resistance**.
- **Why finding is hard:** You cannot do reverse math on a hash output to find the input. The only way to find an input (the block header) that produces a hash starting with 78 zeros is by **brute-force guessing**. Miners must constantly change a random number (the `nonce`) and hash it over and over. This requires massive electrical and computational power.
- **Why verifying is easy:** Hash functions are deterministic and extremely fast to execute. Once a miner finally finds the winning input and broadcasts it, any standard laptop can simply take that exact input, run the double SHA-256 algorithm just once (which technically involves 2 hash calls), and instantly verify that the output indeed starts with 78 zeros. 

---

**Q3: This tx paid ~3,600,000 sat/vB (≈ 6.73 BTC fee for 187 vB!). Look at the date. What was happening, and what does it teach about how fees are set?**

**Answer:**
- **What was happening:** The date was April 20, 2024. This was a historic moment in the Bitcoin network: **Block #840,000**. This block marked the **4th Bitcoin Halving** (where the block reward was cut in half). Simultaneously, it was the launch block for the **Runes Protocol** (a new system for minting tokens on Bitcoin). Thousands of users desperately wanted their transactions to be included in this specific "epic" block to mint the very first Runes.
- **What it teaches about fees:** It clearly teaches that Bitcoin transaction fees are determined by a **Free-Market Auction (Supply and Demand)**. 
  - **Supply:** The block size is strictly limited (only ~1 to 4 MB of space available every 10 minutes).
  - **Demand:** Users attach fees to their transactions. Miners are economically rational, so they always pick transactions with the highest fee rate (`sat/vB`) from the mempool to maximize their own profit.
  - To get into this highly contested block, users had to outbid everyone else, driving the fees to astronomically high levels.

---

**Q4: The coinbase outputs total 4,075,061,499 sat. Subsidy is 312,500,000 sat. Where does the difference come from?**

**Answer:**
- **The calculation:** The difference is $4,075,061,499 - 312,500,000 = 3,762,561,499$ satoshis (approximately 37.6 BTC!).
- **Where it comes from:** This massive difference comes entirely from the **Transaction Fees** paid by regular users.
- **Explanation:** The very first transaction in every block is called the "Coinbase Transaction". This is where the miner claims their reward. The total reward a miner receives consists of two parts:
  1. **The Block Subsidy:** Newly created Bitcoins (which dropped to 3.125 BTC or 312,500,000 satoshis precisely at this halving block).
  2. **The Transaction Fees:** The sum of all the fees paid by every single transaction included in that block. Because this was the highly contested Runes launch block, the transaction fees collected (37.6 BTC) completely dwarfed the actual newly minted subsidy (3.125 BTC).

---

**Q5: Your computed root matches the header exactly. Explain in 2–3 sentences what this proves about the block's transaction list, citing the hash property involved.**

**Answer:**
- **What it proves:** It cryptographically proves that the list of 3,050 transactions you downloaded from the API is **100% authentic and completely unaltered**. 
- **The Hash Property Involved:** This relies on the **Collision Resistance** and **Avalanche Effect** properties of the SHA-256 hash function. If even a single bit of data in any transaction was modified, added, removed, or reordered, its individual transaction ID (`txid`) would completely change. This change would immediately ripple all the way up the Merkle Tree during calculation, resulting in a drastically different final Merkle Root. Because our computed root perfectly matches the one sealed in the block header, we have absolute certainty that the transaction list is exactly what the miner verified.
