"""create phone number col on user column

Revision ID: 853fc1cecec8
Revises: 
Create Date: 2025-10-03 15:29:30.023421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '853fc1cecec8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Step 1 of 2:
def upgrade() -> None:
    """Upgrade schema."""
    # pass
    # sqlalchemy: op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.String(20), nullable=True))

# Step 2 of 2:
def downgrade() -> None:
    """Downgrade schema."""
    # pass
    op.drop_column('users', 'phone_number')