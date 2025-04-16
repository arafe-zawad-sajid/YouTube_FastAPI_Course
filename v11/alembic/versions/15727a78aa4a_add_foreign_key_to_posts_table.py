"""add foreign key to posts table

Revision ID: 15727a78aa4a
Revises: 082b7eaecd0f
Create Date: 2024-07-01 23:43:42.028785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15727a78aa4a'
down_revision: Union[str, None] = '082b7eaecd0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("owner_id", sa.Integer(), nullable=False)
                  )
    op.create_foreign_key("posts_users_fk",  #the constraint is in the source table (posts)
                          source_table="posts", 
                          referent_table="users", 
                          local_cols=["owner_id"],  #col in source table (posts)
                          remote_cols=["id"],  #col in referent table (users)
                          ondelete="CASCADE"
                          )
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
