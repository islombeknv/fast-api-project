"""add few columns to post table

Revision ID: 4a4500437330
Revises: afb124d22a68
Create Date: 2024-09-27 22:58:06.736725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a4500437330'
down_revision: Union[str, None] = 'afb124d22a68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
