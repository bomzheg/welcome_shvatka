"""add topics and messages 2

Revision ID: 5d6a1f03dc49
Revises: 14e58219c03a
Create Date: 2023-05-21 23:06:12.436672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5d6a1f03dc49'
down_revision = '14e58219c03a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(op.f('fk__messages__user_id__users'), 'messages', 'users', ['user_id'], ['id'])
    op.create_foreign_key(op.f('fk__topics__user_id__users'), 'topics', 'users', ['user_id'], ['id'])


def downgrade():
    op.drop_constraint(op.f('fk__topics__user_id__users'), 'topics', type_='foreignkey')
    op.drop_constraint(op.f('fk__messages__user_id__users'), 'messages', type_='foreignkey')
