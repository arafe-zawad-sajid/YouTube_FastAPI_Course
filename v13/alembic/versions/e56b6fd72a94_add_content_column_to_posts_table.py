"""add content column to posts table

Revision ID: e56b6fd72a94
Revises: ecb7eae48357
Create Date: 2024-07-01 23:15:00.288785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e56b6fd72a94'
down_revision: Union[str, None] = 'ecb7eae48357'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String, nullable=False)
                  )
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
