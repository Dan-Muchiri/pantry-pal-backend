"""Add unique constraint on product name and user_id

Revision ID: cb8aab6e9800
Revises: cab0919398e4
Create Date: 2024-07-30 13:52:50.614112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb8aab6e9800'
down_revision = 'cab0919398e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_unique_constraint('unique_product_per_user', ['name', 'user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('unique_product_per_user', type_='unique')

    # ### end Alembic commands ###
