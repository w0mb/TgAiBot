"""add notifications table, drop legacy fields from users

Revision ID: b2a1c3d4e5f6
Revises: 3f6cd3cda96d
Create Date: 2026-05-23 23:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b2a1c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '3f6cd3cda96d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('notifications',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('enable', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('time', sa.String(length=5), nullable=False, server_default='20:00'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name=op.f('notifications_user_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('notifications_pkey')),
    )
    op.drop_column('users', 'notification_enabled')
    op.drop_column('users', 'notification_time')


def downgrade() -> None:
    op.add_column('users', sa.Column('notification_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.add_column('users', sa.Column('notification_time', sa.String(length=5), nullable=False, server_default='20:00'))
    op.drop_constraint(op.f('notifications_user_id_fkey'), 'notifications', type_='foreignkey')
    op.drop_table('notifications')
