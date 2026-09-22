# Q1: Each extra leading zero multiplies expected work by ≈ how much?Why?

**Answer:**

The expected computational workload increases by approximately 16 times for each additional leading zero.

**Why?**
`hexdigest()` represents the SHA-256 hash using hexadecimal characters. Each hexadecimal character has 16 possible values (0–9 and a–f). Therefore, the probability that one character is 0 is:

$$ P(0)=\frac{1}{16} $$

For $k$ leading zeros, the probability of finding a valid hash in one nonce attempt is:

$$ P(\text{success})=\left(\frac{1}{16}\right)^k $$

Therefore, the expected number of attempts is:

$$ E=\frac{1}{P(\text{success})}=16^k $$

If we add one more leading zero, the expected workload changes from $16^k$ to $16^{k+1}$:

$$ \frac{16^{k+1}}{16^k}=16 $$

So, each additional zero makes the expected computational workload approximately 16 times larger.

The actual nonce values may not increase exactly 16 times in every experiment because nonce searching is random. Some trials may find a valid nonce early, while others may take much longer. Over many trials, the average behavior approaches the theoretical expectation of $16^k$.

**Short conclusion:**
Each additional leading zero increases the expected workload by approximately 16×, because each extra zero reduces the probability of success by a factor of 16.

---

# Q2: How many hash calls are needed to verify the found nonce? What does this tell us about PoW?

**Answer:**

**Number of hash calls:** Verifying the found nonce requires only 1 hash call:
$$ \texttt{hashlib.sha256(data + nonce)} $$

**Meaning:** This demonstrates the core property of Proof-of-Work (PoW): asymmetric computational cost.
- **Finding the solution is difficult for the miner:** The miner must try many different nonces and perform a large number of hash computations. For example, when $k=6$, the experiment required more than 24 million hash attempts to find a valid nonce.
- **Verifying the solution is easy for other nodes:** Once a block and its nonce are received, any node only needs to perform one hash computation to check whether the hash satisfies the required condition.

---

# Q3: For n = 1,000,000 transactions, how many hashes does one proof contain?

**Answer:**

A single Merkle proof contains 20 hash values.

**Explanation:**
A Merkle tree is a binary tree, so the length of the proof corresponds to the height of the tree:

$$ h=\lceil \log_2(n)\rceil $$

For $n=1,000,000$:

$$ h=\lceil \log_2(1,000,000)\rceil=20 $$

Therefore, the proof requires 20 sibling hashes.

Each SHA-256 hash is 32 bytes, so the total size of the proof is approximately:

$$ 20\times32=640\text{ bytes} $$

This means that the user does not need to download all 1 million transactions. They only need about 640 bytes of hash data in the Merkle proof to verify that their transaction is included in the Merkle tree.

---

# Q4: Explain one real system that uses exactly this mechanism (SPV, airdrop claim, proof-of-reserves...).

- **Bitcoin SPV (Simplified Payment Verification / Light Client)**: Bitcoin wallets on mobile devices cannot download the entire blockchain because it is very large. Instead, the wallet only needs to download **Block Headers** (which contain the Merkle Root) and request a short **Merkle Proof** from a Full Node to verify that a transaction has been included in a block.
- **Merkle Airdrop (e.g., a Uniswap Airdrop on Ethereum)**: The smart contract only needs to store a single **32-byte hash value**, the **Merkle Root**, representing the entire list of eligible wallets. When a user claims the airdrop, they provide a **Merkle Proof** to prove that their wallet address is included in the eligible list.
- This mechanism significantly reduces the amount of data that needs to be stored directly on the blockchain, thereby **reducing gas costs** compared with storing the entire list of recipients in the smart contract.

---

# Lab 3.3 — Sign, Verify & Recover with eth-account

## Output

```
Địa chỉ ví (Address): 0x2c7536E3605D9C16a7a3D7b1898e529396a65c23

--- TASK 1: Ký thông điệp (Kiểm tra chữ ký) ---
Chữ ký (r, s, v):
r: 0xc466f2dd91c7103ad16c44f11cdb5fe5437882c52f65e3c0915293abd49c22a5
s: 0x7f9db19e52a53e2cb3a5483a83de6bb75e7342047322c201c3fe18936557fd78
v: 28
 Khi chạy lệnh này nhiều lần, chúng ta sẽ thấy chuỗi r, s, v này luôn CỐ ĐỊNH giống hệt nhau.

--- Khôi phục địa chỉ từ chữ ký hợp lệ ---
Địa chỉ khôi phục được : 0x2c7536E3605D9C16a7a3D7b1898e529396a65c23
Khớp với ví ban đầu?   : True

--- TASK 2: Thông điệp bị sửa 1 ký tự (Tính toàn vẹn) ---
Thông điệp sai khôi phục ra địa chỉ: 0x5209C80Aa26044AC61A201141B3ce3AE2bF6db71
Khớp với ví ban đầu?                : False
-> Kết luận Task 2: Vì địa chỉ khôi phục sai hoàn toàn so với gốc, nên phát hiện được dữ liệu bị sửa đổi!
```

## Task 1 — Is the signature identical each run? Which RFC explains this?

**Yes — the signature `(r, s, v)` is identical across multiple runs with the same message.**

**Explanation:**
The `eth-account` library uses **deterministic ECDSA** as specified in **RFC 6979**. Instead of picking a random nonce `k` each time (which would produce a different signature every run), RFC 6979 derives `k` deterministically from the **private key** and the **message hash** using an HMAC-DRBG construction. This guarantees that the same `(private_key, message)` pair always produces the exact same `(r, s)` values.

**Why this matters:**
- **Security:** Non-deterministic `k` is dangerous — if two different messages are signed with the same random `k`, the private key can be mathematically extracted. RFC 6979 eliminates this risk.
- **Reproducibility:** The output is verifiable and predictable without sacrificing security.

## Task 2 — Tampered message recovers a different address. Why does this prove integrity?

**Observation:** Changing just one character (`"Buoi 3"` → `"Buoi 4"`) causes `recover_message` to output a completely different Ethereum address (`0x5209C80A...` instead of `0x2c7536E3...`), which does **not** match the original wallet.

**Why this proves integrity:**
ECDSA signature verification works by inverting the signing equation to reconstruct the public key (and thus the Ethereum address) from `(message_hash, r, s, v)`:

$$\text{address} = \text{recover}(\text{hash}(m),\ r,\ s,\ v)$$

When the message `m` is tampered, `hash(m')` is completely different (avalanche effect of Keccak-256). The recovery formula then yields a **random, unrelated address** — not the signer's address. Since there is no known private key for that recovered address, the tampering is immediately detectable.

**Conclusion:** The signature is cryptographically bound to both the **private key** and the **exact message content**. Any modification — even a single character — produces a mismatch that any verifier can detect without knowing the private key.
