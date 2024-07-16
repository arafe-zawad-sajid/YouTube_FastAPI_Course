"""create posts table

Revision ID: ecb7eae48357
Revises: 
Create Date: 2024-07-01 17:39:03.670191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecb7eae48357'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#Runs the command for making the changes 
#We put all of the logic for creating "posts" table
#  
def upgrade() -> None:
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable=True, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False)
                    )
    pass

#To handle the rollback
#  
# 
def downgrade() -> None:
    op.drop_table("posts")
    pass
