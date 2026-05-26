import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
import datetime
from ..extensions import db
from ..models import Transaction
from ..config import Config
from .categorizer import categorize


def get_plaid_client():
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox if Config.PLAID_ENV == "sandbox" else plaid.Environment.Production,
        api_key={"clientId": Config.PLAID_CLIENT_ID, "secret": Config.PLAID_SECRET}
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)


def sync_transactions(user, days_back=30):
    client = get_plaid_client()
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_back)

    request = TransactionsGetRequest(
        access_token=user.plaid_access_token,
        start_date=start_date,
        end_date=end_date,
        options=TransactionsGetRequestOptions(count=500)
    )

    response = client.transactions_get(request)
    new_count = 0

    for txn in response["transactions"]:
        existing = Transaction.query.filter_by(
            plaid_transaction_id=txn["transaction_id"]
        ).first()

        if not existing:
            new_txn = Transaction(
                user_id=user.id,
                plaid_transaction_id=txn["transaction_id"],
                amount=txn["amount"],
                name=txn["name"],
                category=categorize(txn),
                date=txn["date"]
            )
            db.session.add(new_txn)
            new_count += 1

    db.session.commit()
    return new_count
