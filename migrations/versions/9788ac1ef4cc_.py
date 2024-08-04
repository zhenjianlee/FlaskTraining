"""empty message

Revision ID: 9788ac1ef4cc
Revises: 
Create Date: 2024-08-04 20:48:18.689291

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9788ac1ef4cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_index('name')

    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.alter_column('store_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=mysql.VARCHAR(length=80),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.TEXT(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=mysql.TEXT(),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=80),
               existing_nullable=False)

    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('store_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.create_index('name', ['name'], unique=True)

    # ### end Alembic commands ###