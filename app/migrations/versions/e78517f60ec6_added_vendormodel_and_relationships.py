"""Added VendorModel and relationships

Revision ID: e78517f60ec6
Revises: 9deb3a509139
Create Date: 2024-08-09 10:59:26.518595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e78517f60ec6'
down_revision: Union[str, None] = '9deb3a509139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create vendors table
    op.create_table(
        'vendors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Add vendor_id column to products table
    op.add_column('products', sa.Column('vendor_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_products_vendor_id', 'products', 'vendors', ['vendor_id'], ['id'])

def downgrade():
    # Drop the foreign key and vendor_id column from products table
    op.drop_constraint('fk_products_vendor_id', 'products', type_='foreignkey')
    op.drop_column('products', 'vendor_id')

    # Drop vendors table
    op.drop_table('vendors')