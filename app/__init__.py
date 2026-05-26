from flask import Flask
from .config import Config
from .extensions import db, migrate


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth import auth_bp
    from .routes.transactions import transactions_bp
    from .routes.budgets import budgets_bp
    from .routes.plaid import plaid_bp
    from .routes.assistant import assistant_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(budgets_bp, url_prefix="/budgets")
    app.register_blueprint(plaid_bp, url_prefix="/plaid")
    app.register_blueprint(assistant_bp, url_prefix="/assistant")

    return app
