"""delete notifications

Revision ID: 3f6cd3cda96d
Revises: a01813c1da71
Create Date: 2026-05-23 23:00:57.642662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3f6cd3cda96d'
down_revision: Union[str, Sequence[str], None] = 'a01813c1da71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f('users_notification_id_fkey'), 'users', type_='foreignkey')
    op.drop_column('users', 'notification_id')
    op.add_column('users', sa.Column('notification_enabled', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.add_column('users', sa.Column('notification_time', sa.String(length=5), nullable=False, server_default='12:00'))
    op.drop_table('notifications')


def downgrade() -> None:
    op.create_table('notifications',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('enable', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('notifications_user_id_fkey')),
        sa.PrimaryKeyConstraint('id', name=op.f('notifications_pkey')),
    )
    op.add_column('users', sa.Column('notification_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(op.f('users_notification_id_fkey'), 'users', 'notifications', ['notification_id'], ['id'])
    op.drop_column('users', 'notification_time')
    op.drop_column('users', 'notification_enabled')
