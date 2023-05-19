"""fix tg id int->bigint

Revision ID: 91a41238f13f
Revises: 56df5c6b0df6
Create Date: 2023-05-19 21:25:41.736618

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '91a41238f13f'
down_revision = '56df5c6b0df6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('chats', 'tg_id', existing_type=sa.BIGINT())
    op.alter_column('users', 'tg_id', existing_type=sa.BIGINT())


def downgrade():
    pass
