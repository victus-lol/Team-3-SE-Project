"""Add persistent login throttling state.

Revision ID: 61c8a4209f20
Revises: a2c3aecd885d
Create Date: 2026-11-12
"""

import sqlalchemy as sa
from alembic import op

revision = "61c8a4209f20"
down_revision = "a2c3aecd885d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "login_attempts",
        sa.Column("key_hash", sa.String(length=64), nullable=False),
        sa.Column("failure_count", sa.Integer(), nullable=False),
        sa.Column("window_started_at", sa.Float(), nullable=False),
        sa.Column("locked_until", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("key_hash"),
    )


def downgrade():
    op.drop_table("login_attempts")
