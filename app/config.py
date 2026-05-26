import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret-change-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://localhost/maya")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLAID_CLIENT_ID = os.environ.get("PLAID_CLIENT_ID")
    PLAID_SECRET = os.environ.get("PLAID_SECRET")
    PLAID_ENV = os.environ.get("PLAID_ENV", "sandbox")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    JWT_EXPIRATION_HOURS = 24
