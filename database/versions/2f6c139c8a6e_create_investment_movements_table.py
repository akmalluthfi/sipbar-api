"""create investment movements table

Revision ID: 2f6c139c8a6e
Revises: a5643812216b
Create Date: 2025-10-20 13:21:17.047506

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = "2f6c139c8a6e"
down_revision: Union[str, Sequence[str], None] = "a5643812216b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "investment_movements",
        sa.Column("id", UUID(), primary_key=True),
        sa.Column("item_code", sa.String(50), nullable=False),
        sa.Column("item", sa.String(255), nullable=False),
        sa.Column("opening_stock", sa.Integer, nullable=False),
        sa.Column("stock_in", sa.Integer, nullable=False),
        sa.Column("stock_out", sa.Integer, nullable=False),
        sa.Column("net_stock_change", sa.Integer, nullable=False),
        sa.Column("closing_stock", sa.Integer, nullable=False),
        sa.Column("closing_value", sa.Integer, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("priority_category", sa.String(2), nullable=False),
        sa.Column("cluster_category", sa.String(2), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("investment_movements")
