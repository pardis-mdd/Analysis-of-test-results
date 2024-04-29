"""Added firstname and lastname fields to User model

Revision ID: ec3311232527
Revises: 6ed310b7f013
Create Date: 2024-04-15 20:54:20.964750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec3311232527'
down_revision = '6ed310b7f013'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('lastname', sa.String(length=64), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('lastname')
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###