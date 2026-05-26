# maya-finance-api

backend for Maya, my personal finance iOS app. pulls real bank transactions through Plaid, categorizes them, runs an AI budget assistant on top, and serves it all through a JWT protected REST API to a Swift UIKit frontend.

## architecture

```
iOS (Swift UIKit)
   │
   ▼  HTTPS + JWT
Flask API on AWS EC2 (gunicorn + nginx)
   │
   ├─ Plaid API for live bank transactions
   ├─ PostgreSQL for users, transactions, budgets
   ├─ Firebase for identity and tokens
   └─ Gemini API for the budget assistant
```

## endpoints

| method | route | what it does |
|--------|-------|-------------|
| POST | /auth/register | hash password and create user |
| POST | /auth/login | return JWT |
| POST | /plaid/link | exchange Plaid public token |
| GET  | /transactions | fetch and categorize transactions |
| GET  | /budgets/summary | spending breakdown by category |
| POST | /assistant/chat | budget assistant chatting over your transaction history |

## the hard part

merchant categorization. the same Starbucks transaction comes back from different banks as Starbucks, SBUX, Starbucks #4421, STARBUCKS COFFEE, and about ten other variants. regex got me 60% of the way there before turning into a nightmare. ended up writing a fuzzy matching layer that normalizes merchant strings then uses Levenshtein distance to collapse variants into a single canonical merchant. Plaid's sandbox also doesn't match production data shapes, so categorization that passed every dev test broke immediately on real bank data. lots of overnight rewrites.

## run it locally

```bash
git clone https://github.com/jashkaransingh/maya-finance-api
cd maya-finance-api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 -m flask run
```

env vars

`DATABASE_URL`, `JWT_SECRET`, `PLAID_CLIENT_ID`, `PLAID_SECRET`, `GEMINI_API_KEY`, `FIREBASE_CREDENTIALS`

## stack

Flask, PostgreSQL via psycopg2, Plaid API, Firebase identity, JWT, Gemini API, gunicorn + nginx, deployed on AWS EC2.
