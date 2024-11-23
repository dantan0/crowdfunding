from xrpl.clients import WebsocketClient
from xrpl.models import Subscribe, IssuedCurrencyAmount, Payment, AccountLines
from xrpl.utils import xrp_to_drops
from wallet import investor_wallet, campaign_wallet, Rpc_client
from xrpl.transaction import submit_and_wait

# 100,000 equals 50% stake of a company
EQUITY_TOKEN = 10000000
TOTAL_AMOUNT = 100000 # in xrp, not in drops

url = "wss://s.altnet.rippletest.net/"
req = Subscribe(accounts=[investor_wallet.address])
with WebsocketClient(url) as client:
    client.send(req)
    for message in client:
        if "tx_json" in message and message["tx_json"]["TransactionType"] == "Payment" and message["tx_json"]['Destination'] == campaign_wallet.address:
            amount_received = int(message["tx_json"]["DeliverMax"])
            # print('amount received', amount_received)
            total_drops = int(xrp_to_drops(TOTAL_AMOUNT))
            # print('total drops', total_drops)
            number_of_tokens = (amount_received / total_drops) * EQUITY_TOKEN
            # print('number of tokens', number_of_tokens)

            # campaigning wallet is the sending wallet
            # investor wallet is the destination
            send_currency_tx = Payment(
                account=campaign_wallet.address,
                amount=IssuedCurrencyAmount(
                    currency="ABC",
                    value=int(number_of_tokens),
                    issuer=campaign_wallet.address
                ),
                destination=investor_wallet.address
            )
            token_response = submit_and_wait(send_currency_tx, Rpc_client, campaign_wallet)
            account_response = Rpc_client.request(AccountLines(
                account=investor_wallet.address,
                ledger_index="validated"
            ))
            print("token balance: ", account_response.result['balance'])


