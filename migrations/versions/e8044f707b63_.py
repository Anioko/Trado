"""empty message

Revision ID: e8044f707b63
Revises: 
Create Date: 2022-07-25 20:42:07.598312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8044f707b63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('portfolio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=80), nullable=True),
    sa.Column('image', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint(None, 'seeking', type_='foreignkey')
    op.create_foreign_key(None, 'seeking', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.add_column('users', sa.Column('is_public', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_users_is_public'), 'users', ['is_public'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_is_public'), table_name='users')
    op.drop_column('users', 'is_public')
    op.drop_constraint(None, 'seeking', type_='foreignkey')
    op.create_foreign_key(None, 'seeking', 'users', ['user_id'], ['id'])
    op.drop_table('portfolio')
    # ### end Alembic commands ###
