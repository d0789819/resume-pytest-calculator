import os

import pytest

from app import create_app
from app.database import db


@pytest.fixture()
def app(tmp_path):
    database_url = os.getenv(
        "TEST_DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}"
    )
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": database_url,
            "AUDIT_SERVICE_URL": "https://audit.example.test/events",
        }
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
