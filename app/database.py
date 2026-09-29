"""Database extension and models."""

from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
TW_TIMEZONE = timezone(timedelta(hours=8))

def taipei_now() -> datetime:
    return datetime.now(TW_TIMEZONE)

class Calculation(db.Model):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation: Mapped[str] = mapped_column(String(20), nullable=False)
    a: Mapped[float] = mapped_column(Float, nullable=False)
    b: Mapped[float] = mapped_column(Float, nullable=False)
    result: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=taipei_now,
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "operation": self.operation,
            "a": self.a,
            "b": self.b,
            "result": self.result,
            "created_at": self.created_at.isoformat(),
        }
