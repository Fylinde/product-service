"""Added interactions relationship to ProductModel

Revision ID: 9deb3a509139
Revises: 6d5500712883
Create Date: 2024-08-09 09:10:46.136125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9deb3a509139'
down_revision: Union[str, None] = '6d5500712883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding a foreign key if needed
    op.create_foreign_key('fk_user_interactions_product_id', 'user_interactions', 'products', ['product_id'], ['id'])

def downgrade() -> None:
    # Dropping the foreign key during downgrade
    op.drop_constraint('fk_user_interactions_product_id', 'user_interactions', type_='foreignkey')
