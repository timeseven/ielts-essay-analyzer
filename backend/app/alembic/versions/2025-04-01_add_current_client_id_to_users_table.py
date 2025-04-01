"""add current_client_id to users table

Revision ID: 666ca9cd8fb1
Revises: ad3ff34d8265
Create Date: 2025-04-01 14:04:22.047210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '666ca9cd8fb1'
down_revision: Union[str, None] = 'ad3ff34d8265'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('current_client_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'users', 'clients', ['current_client_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'current_client_id')
    # ### end Alembic commands ###
