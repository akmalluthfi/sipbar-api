"""create investment records table

Revision ID: a5643812216b
Revises:
Create Date: 2025-10-20 13:10:27.521984

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = "a5643812216b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "investment_records",
        sa.Column("id", UUID(), primary_key=True),
        sa.Column("document_number", sa.String(50), nullable=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("item_code", sa.String(50), nullable=False),
        sa.Column("item", sa.String(255), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("department", sa.String(50), nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("investment_records")
