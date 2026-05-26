# maya-finance-api

Backend for **Maya**, a personal finance iOS app. Pulls real transaction data via Plaid, categorizes spending, stores everything in PostgreSQL, and exposes a clean REST API to a Swift/UIKit frontend.

## Architecture

```
iOS (Swift/UIKit)
      │
      ▼ HTTPS + JWT
Flask REST API
      │
      ├── Plaid API ──── real-time bank transactions
      ├── PostgreSQL ─── user data, transactions, budgets
      └── Gemini API ─── AI budget assistant
```

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/auth/register` | Register user, hash password |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/plaid/link` | Exchange Plaid public token |
| GET | `/transactions` | Fetch + categorize recent transactions |
| GET | `/budgets/summary` | Spending breakdown by category |
| POST | `/assistant/chat` | AI budget assistant (RAG over transactions) |

## Setup

```bash
git clone https://github.com/jashkaransingh/maya-finance-api
cd maya-finance-api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
python3 -m flask run
```

**Required env vars:** `DATABASE_URL`, `JWT_SECRET`, `PLAID_CLIENT_ID`, `PLAID_SECRET`, `GEMINI_API_KEY`

## Stack

- **Flask** — REST API, routing, middleware
- **PostgreSQL** — transactions, users, budgets (psycopg2)
- **Plaid API** — bank data aggregation
- **JWT** — stateless auth on all protected routes
- **Gemini API** — budget assistant natural language layer
- **AWS EC2** — deployed with gunicorn + nginx
