"""'Init'

Revision ID: a2b2b23a4286
Revises: bcca2a6606b9
Create Date: 2023-06-17 19:50:16.543551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2b2b23a4286'
down_revision = 'bcca2a6606b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('phone_number', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'phone_number')
    # ### end Alembic commands ###
