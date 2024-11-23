from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.clients import JsonRpcClient

# Create a client to connect to the test network
Rpc_client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# Create two wallets to send money between on the test network
campaign_wallet = Wallet.from_seed('sEdSR3bzcjcPByR8debuEZHyy2Sm54M')
investor_wallet = Wallet.from_seed('sEdVH4JYKA51VHhUdnVc4AhuhJ82AbU')
# print(campaign_wallet.seed)
