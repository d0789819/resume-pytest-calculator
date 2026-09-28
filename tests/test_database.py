import os
from datetime import timedelta

from sqlalchemy import text

from app.database import Calculation, db, taipei_now


def test_application_time_uses_gmt_plus_8():
    now = taipei_now()

    assert now.utcoffset() == timedelta(hours=8)


def test_database_connection_uses_expected_backend(app):
    with app.app_context():
        assert db.session.execute(text("SELECT 1")).scalar_one() == 1
        expected_backend = "postgresql" if os.getenv("TEST_DATABASE_URL") else "sqlite"
        assert db.engine.url.get_backend_name() == expected_backend


def test_calculation_is_persisted(app):
    with app.app_context():
        record = Calculation(operation="add", a=10, b=5, result=15)
        db.session.add(record)
        db.session.commit()
        record_id = record.id

        db.session.remove()
        loaded = db.session.get(Calculation, record_id)

        assert loaded is not None
        assert loaded.result == 15
