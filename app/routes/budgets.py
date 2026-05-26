from flask import Blueprint, jsonify, g
from sqlalchemy import func
from ..middleware.auth import require_auth
from ..models import Transaction
import datetime

budgets_bp = Blueprint("budgets", __name__)


@budgets_bp.route("/summary", methods=["GET"])
@require_auth
def summary():
    # Current month spending by category
    now = datetime.date.today()
    start_of_month = now.replace(day=1)

    rows = (
        Transaction.query
        .filter(
            Transaction.user_id == g.user.id,
            Transaction.date >= start_of_month
        )
        .with_entities(Transaction.category, func.sum(Transaction.amount).label("total"))
        .group_by(Transaction.category)
        .all()
    )

    breakdown = {row.category: round(row.total, 2) for row in rows}
    total = round(sum(breakdown.values()), 2)

    return jsonify({
        "month": str(start_of_month),
        "total_spent": total,
        "by_category": breakdown
    }), 200
