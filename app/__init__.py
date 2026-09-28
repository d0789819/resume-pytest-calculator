"""Flask application factory."""

import os

from flask import Flask
from flask_migrate import Migrate

from app.database import db
from app.routes import api

migrate = Migrate()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", "sqlite:///calculations.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        AUDIT_SERVICE_URL=os.getenv("AUDIT_SERVICE_URL", ""),
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api)

    return app
