"""add group_invitations table

Revision ID: e6f1a89c10d2
Revises: b9e5c824e276
Create Date: 2026-07-25 20:33:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e6f1a89c10d2'
down_revision: Union[str, Sequence[str], None] = 'b9e5c824e276'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'group_invitations',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('group_id', sa.BigInteger(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('invited_by', sa.BigInteger(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column(
            'status',
            sa.Enum('pending', 'accepted', 'expired', name='invitationstatus'),
            server_default='pending',
            nullable=False
        ),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['Group.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )


def downgrade() -> None:
    op.drop_table('group_invitations')
    op.execute('DROP TYPE invitationstatus;')
