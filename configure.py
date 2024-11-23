from xrpl.models import Payment, Tx, Subscribe, TrustSet, IssuedCurrencyAmount, AccountSet, AccountSetAsfFlag
from xrpl.transaction import submit_and_wait
from wallet import investor_wallet, campaign_wallet, Rpc_client as client


def configure_account(client, campaign_wallet):
    account_set_tx = AccountSet(
        account=campaign_wallet.classic_address,
        set_flag=AccountSetAsfFlag.ASF_DEFAULT_RIPPLE
    )
    response = submit_and_wait(account_set_tx, client, campaign_wallet)
    print(response)

configure_account(client, campaign_wallet)
