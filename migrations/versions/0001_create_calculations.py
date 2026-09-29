"""Create the calculations table.

Revision ID: 0001_calculations
Revises:
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_calculations"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "calculations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("operation", sa.String(length=20), nullable=False),
        sa.Column("a", sa.Float(), nullable=False),
        sa.Column("b", sa.Float(), nullable=False),
        sa.Column("result", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade():
    op.drop_table("calculations")
