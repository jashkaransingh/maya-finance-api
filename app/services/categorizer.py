# Maps Plaid's category hierarchy to simplified budget categories
PLAID_TO_CATEGORY = {
    "Food and Drink": "food",
    "Travel": "travel",
    "Shops": "shopping",
    "Recreation": "entertainment",
    "Healthcare": "health",
    "Service": "utilities",
    "Transfer": "transfer",
    "Payment": "payment",
    "Bank Fees": "fees",
}


def categorize(plaid_txn):
    """
    Takes a raw Plaid transaction dict and returns a simplified category string.
    Plaid returns categories as a list from broad to specific: ["Food and Drink", "Restaurants"]
    """
    categories = plaid_txn.get("category", [])
    if not categories:
        return "other"

    top_level = categories[0]
    return PLAID_TO_CATEGORY.get(top_level, "other")
