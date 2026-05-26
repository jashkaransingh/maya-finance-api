from flask import Blueprint, jsonify, g
from ..middleware.auth import require_auth
from ..models import Transaction
from ..services.plaid_service import sync_transactions
from ..services.categorizer import categorize

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("", methods=["GET"])
@require_auth
def get_transactions():
    # Pull latest from Plaid and sync to DB
    if g.user.plaid_access_token:
        new_txns = sync_transactions(g.user)

    txns = (Transaction.query
            .filter_by(user_id=g.user.id)
            .order_by(Transaction.date.desc())
            .limit(100)
            .all())

    return jsonify({"transactions": [t.to_dict() for t in txns]}), 200
