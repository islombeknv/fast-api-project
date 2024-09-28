"""create user table

Revision ID: 6f1eec4a6083
Revises: cb26e5f3873e
Create Date: 2024-09-27 22:09:37.801635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f1eec4a6083'
down_revision: Union[str, None] = 'cb26e5f3873e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')          
                    )


def downgrade() -> None:
    op.drop_table('users')
