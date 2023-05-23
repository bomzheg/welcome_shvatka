"""add topics and messages

Revision ID: 14e58219c03a
Revises: 91a41238f13f
Create Date: 2023-05-20 20:44:34.061598

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '14e58219c03a'
down_revision = '91a41238f13f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('user_message_id', sa.BigInteger(), nullable=False),
        sa.Column('forum_message_id', sa.BigInteger(), nullable=False),
        sa.Column('from_admin', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__messages')),
        sa.UniqueConstraint(
            'user_id', 'user_message_id', 'forum_message_id',
            name='unique_messages_ids_combinations',
        )
    )
    op.create_table(
        'topics',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('start_message_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk__topics')),
        sa.UniqueConstraint('user_id', 'topic_id', name='unique_topics_pairs')
    )


def downgrade():
    op.drop_table('topics')
    op.drop_table('messages')
