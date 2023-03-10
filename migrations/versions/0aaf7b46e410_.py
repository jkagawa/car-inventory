"""empty message

Revision ID: 0aaf7b46e410
Revises: 957afca40bb2
Create Date: 2023-02-26 15:06:21.919646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aaf7b46e410'
down_revision = '957afca40bb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('make', sa.String(length=100), nullable=False),
    sa.Column('model', sa.String(length=100), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('user_token', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_token'], ['user.token'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('user', 'g_auth_verify',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('user', 'token',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'token',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'g_auth_verify',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_table('car')
    # ### end Alembic commands ###
