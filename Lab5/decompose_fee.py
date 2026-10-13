from web3 import Web3

try:
    from web3.middleware import ExtraDataToPOAMiddleware
except ImportError:
    from web3.middleware import geth_poa_middleware as ExtraDataToPOAMiddleware

RPC_URL = "https://l1testnet.trustkeys.network"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

try:
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
except Exception:
    pass

h = "0x5e6796d0ef53864bc0b82491137c39a2273d340ebfae8272f642b8e938f01826" #id giao dich,len metamask để đọc chi tiết giao dịch,so sánh với kqua true khi chạy code
rcpt = w3.eth.get_transaction_receipt(h)
tx   = w3.eth.get_transaction(h)
blk  = w3.eth.get_block(rcpt["blockNumber"])

base_fee  = blk.get("baseFeePerGas", 0)
gas_used  = rcpt["gasUsed"]
eff_price = rcpt["effectiveGasPrice"]         # baseFee + min(tip, maxFee - baseFee)
paid   = gas_used * eff_price
burned = gas_used * base_fee                   # leaves circulation / rời lưu thông
tip    = gas_used * (eff_price - base_fee)     # to the block proposer / về proposer

print("=== LAB 5.3 - DECOMPOSE TYPE-2 TRANSACTION FEE ===")
print(f"Tx Hash:           {h}")
print(f"Block Number:      {rcpt['blockNumber']}")
print(f"Gas Used:          {gas_used:,}")
print(f"Base Fee per Gas:  {base_fee} wei ({base_fee / 1e9:.9f} gwei)")
print(f"Effective Price:   {eff_price:,} wei ({eff_price / 1e9:.9f} gwei)")
print(f"Max Fee per Gas:   {tx.get('maxFeePerGas', 0):,} wei")
print(f"Max Priority Fee:  {tx.get('maxPriorityFeePerGas', 0):,} wei")
print("-" * 50)
print(f"Total Paid:        {paid} wei ({paid / 1e18:.18f} coin)")
print(f"Burned:            {burned} wei ({burned / 1e18:.18f} coin)  [leaves circulation]")
print(f"Tip (Miner fee):   {tip} wei ({tip / 1e18:.18f} coin)  [to proposer]")
print(f"\nIdentity check:    paid == burned + tip ? -> {paid == burned + tip}")
print(f"Equation:          {paid} == {burned} + {tip}")
