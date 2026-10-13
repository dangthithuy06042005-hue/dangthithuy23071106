import sys
from web3 import Web3

# web3.py v6 vs v7 compatibility for ExtraDataToPOAMiddleware
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

if not w3.is_connected():
    print(f"Error: Khong the ket noi toi RPC {RPC_URL}")
    sys.exit(1)

latest_block = w3.eth.get_block("latest")
chain_id = w3.eth.chain_id

print(f"Connected to TrustKeys L1  chainId={chain_id}  head block={latest_block['number']}")
print("[eth_getBlockByNumber latest]")
print(f"  number        = {latest_block['number']}")
print(f"  gasLimit      = {latest_block['gasLimit']:,}")
gas_used_pct = (latest_block['gasUsed'] / latest_block['gasLimit']) * 100
print(f"  gasUsed       = {latest_block['gasUsed']:,}  ({gas_used_pct:.2f}% full)")
base_fee = latest_block.get('baseFeePerGas', 0)
print(f"  baseFeePerGas = {base_fee}  ({base_fee / 1e9:.9f} gwei ({base_fee} wei))  <- EIP-1559 active")
print(f"  #txs          = {len(latest_block['transactions'])}")

print("\n[eth_feeHistory]  last 20 blocks (base fee series)")
print(f"  {'block':<10} {'baseFee(gwei)':<15} {'gasUsedRatio':<15} {'tip p50 (gwei)':<15}")

fh = w3.eth.fee_history(20, "latest", [10, 50, 90])
oldest = fh["oldestBlock"]
gas_ratios = fh["gasUsedRatio"]

for i, b_fee in enumerate(fh["baseFeePerGas"][:-1]):
    blk_num = oldest + i
    ratio = gas_ratios[i] * 100
    tip_p50 = (fh["reward"][i][1] / 1e9) if "reward" in fh and i < len(fh["reward"]) and len(fh["reward"][i]) > 1 else 0.0
    print(f"  {blk_num:<10} {b_fee / 1e9:<15.4f} {ratio:<14.2f}% {tip_p50:<15.4f}")

next_base = fh["baseFeePerGas"][-1]
avg_ratio = sum(gas_ratios) / len(gas_ratios) * 100
verdict = "quiet" if avg_ratio < 50 else "BUSY"

print(f"  next block's projected baseFee = {next_base / 1e9:.9f} gwei ({next_base} wei)")
print(f"  average gasUsedRatio over window = {avg_ratio:.2f}%  -> chain is {verdict}")
