"""Add column to table USERS

Revision ID: 3a9e67961169
Revises: 9418b4905f20
Create Date: 2024-06-26 08:46:57.046673

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3a9e67961169"
down_revision: Union[str, None] = "9418b4905f20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("Проверка", sa.String(), nullable=False, server_default="оаоао"),
    )


def downgrade() -> None:
    op.drop_column("users", "Проверка")
