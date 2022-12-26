"""edit name in temp_inventory_card

Revision ID: 80dd68a5b694
Revises: 51107170e994
Create Date: 2022-12-26 13:56:25.233929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80dd68a5b694'
down_revision = '51107170e994'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("temp_inventory_card", "room_uid_id", new_column_name="room_uid")


def downgrade() -> None:
    pass
