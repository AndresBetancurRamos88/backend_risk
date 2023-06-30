"""empty message

Revision ID: 06e12a893c98
Revises: bac5cf190b10
Create Date: 2023-06-29 19:24:21.509899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06e12a893c98'
down_revision = 'bac5cf190b10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('risks_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.drop_column('descripcion')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('risks_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descripcion', sa.TEXT(), nullable=True))
        batch_op.drop_column('description')

    # ### end Alembic commands ###
