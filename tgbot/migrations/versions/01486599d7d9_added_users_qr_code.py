"""added users qr code

Revision ID: 01486599d7d9
Revises: e996159ce98d
Create Date: 2022-09-28 16:55:15.912498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01486599d7d9'
down_revision = 'e996159ce98d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriber', sa.Column('qr_code_img_path', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriber', 'qr_code_img_path')
    # ### end Alembic commands ###
