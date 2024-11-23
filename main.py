from xrpl.account import get_balance
from xrpl.clients import JsonRpcClient, WebsocketClient
from xrpl.utils import xrp_to_drops
from xrpl.models import Payment, Tx, Subscribe, TrustSet, IssuedCurrencyAmount, AccountSet, AccountSetAsfFlag
from xrpl.transaction import submit_and_wait
from wallet import investor_wallet, campaign_wallet, Rpc_client as client

# Both balances should be zero since nothing has been sent yet
print("Balances of wallets before Payment tx")
print(get_balance(investor_wallet.address, client))
print(get_balance(campaign_wallet.address, client))

# in this case, receiver is the investor_wallet, issuer is the campaign_wallet
trustline_tx = TrustSet(
    account=investor_wallet.address, 
    limit_amount=IssuedCurrencyAmount(
        currency="ABC",
        value="10000000",
        issuer=campaign_wallet.address
    )
)

trustline_response = submit_and_wait(trustline_tx, client, investor_wallet)

# Create a Payment transaction from wallet1 to wallet2
payment_tx = Payment(
    account=investor_wallet.address,
    amount=xrp_to_drops(0.01),
    destination=campaign_wallet.address,
)

# Submit the payment to the network and wait to see a response
#   Behind the scenes, this fills in fields which can be looked up automatically like the fee.
#   It also signs the transaction with wallet1 to prove you own the account you're paying from.
payment_response = submit_and_wait(payment_tx, client, investor_wallet)
print("Transaction was submitted")

# Create a "Tx" request to look up the transaction on the ledger
tx_response = client.request(Tx(transaction=payment_response.result["hash"]))

# Check whether the transaction was actually validated on ledger
print("Validated:", tx_response.result["validated"])

# Check balances after 1000 drops (.001 XRP) was sent from wallet1 to wallet2
print("Balances of wallets after Payment tx:")
print(get_balance(investor_wallet.address, client))
print(get_balance(campaign_wallet.address, client))
