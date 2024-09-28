"""add content column to post

Revision ID: cb26e5f3873e
Revises: 5f1369ef8727
Create Date: 2024-09-27 21:59:19.634109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb26e5f3873e'
down_revision: Union[str, None] = '5f1369ef8727'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
