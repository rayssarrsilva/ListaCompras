"""add status column to cart

Revision ID: 209c559f9a4e
Revises: 
Create Date: 2025-11-13 15:28:56.966167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '209c559f9a4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('cart', sa.Column('status', sa.String(length=20), nullable=False, server_default="open"))

def downgrade():
    op.drop_column('cart', 'status')