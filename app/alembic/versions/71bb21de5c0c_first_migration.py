"""First migration

Revision ID: 71bb21de5c0c
Revises: ebc50e28c201
Create Date: 2023-01-10 14:21:59.980725

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '71bb21de5c0c'
down_revision = 'ebc50e28c201'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_chat',
    sa.Column('uid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('chat_uid', sa.Integer(), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('uid')
    )
    op.create_unique_constraint(None, 'departments', ['uid'])
    op.create_unique_constraint(None, 'employee', ['uid'])
    op.create_unique_constraint(None, 'inventory_card', ['uid'])
    op.create_unique_constraint(None, 'inventory_info', ['uid'])
    op.create_unique_constraint(None, 'movements', ['uid'])
    op.create_unique_constraint(None, 'object_types', ['uid'])
    op.create_unique_constraint(None, 'rooms', ['uid'])
    op.create_unique_constraint(None, 'temp_inventory_card', ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'temp_inventory_card', type_='unique')
    op.drop_constraint(None, 'rooms', type_='unique')
    op.drop_constraint(None, 'object_types', type_='unique')
    op.drop_constraint(None, 'movements', type_='unique')
    op.drop_constraint(None, 'inventory_info', type_='unique')
    op.drop_constraint(None, 'inventory_card', type_='unique')
    op.drop_constraint(None, 'employee', type_='unique')
    op.drop_constraint(None, 'departments', type_='unique')
    op.drop_table('telegram_chat')
    # ### end Alembic commands ###
