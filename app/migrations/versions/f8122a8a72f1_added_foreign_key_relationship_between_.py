"""Added foreign key relationship between Product and Vendor

Revision ID: f8122a8a72f1
Revises: e78517f60ec6
Create Date: 2024-08-09 11:57:10.931362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8122a8a72f1'
down_revision: Union[str, None] = 'e78517f60ec6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Creating foreign key constraint linking products.vendor_id to vendors.id
    op.create_foreign_key('fk_products_vendor_id_vendors', 'products', 'vendors', ['vendor_id'], ['id'])


def downgrade() -> None:
    # Dropping the foreign key constraint
    op.drop_constraint('fk_products_vendor_id_vendors', 'products', type_='foreignkey')
