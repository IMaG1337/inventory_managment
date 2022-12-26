"""added unique in inventory_card

Revision ID: 51107170e994
Revises: 15d4687ac5fe
Create Date: 2022-12-26 12:50:13.899388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51107170e994'
down_revision = '15d4687ac5fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_inventory_info_uid", "inventory_card", ["inventory_info_uid"])



def downgrade() -> None:
    pass
