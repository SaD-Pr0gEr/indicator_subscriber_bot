"""initial

Revision ID: eca710772ee4
Revises: 
Create Date: 2022-09-22 10:22:03.531456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eca710772ee4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriber',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('is_moderator', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('Id'),
    sa.UniqueConstraint('tg_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriber')
    # ### end Alembic commands ###
