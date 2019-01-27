"""empty message

Revision ID: 36c809159664
Revises: f21e0d00de32
Create Date: 2019-01-26 14:06:38.348476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36c809159664'
down_revision = 'f21e0d00de32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coasterparks', sa.Column('address', sa.String(length=100), nullable=True))
    op.add_column('coasterparks', sa.Column('openDate', sa.String(length=40), nullable=True))
    op.add_column('coasterparks', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('coasterparks', sa.Column('statusDate', sa.String(length=40), nullable=True))
    op.add_column('coasterrides', sa.Column('coasterOrRide', sa.Boolean(), nullable=True))
    op.add_column('coasterrides', sa.Column('coasterType', sa.String(length=500), nullable=True))
    op.add_column('coasterrides', sa.Column('configuration', sa.String(length=500), nullable=True))
    op.add_column('coasterrides', sa.Column('make', sa.String(length=500), nullable=True))
    op.add_column('coasterrides', sa.Column('modelCategory', sa.String(length=500), nullable=True))
    op.add_column('coasterrides', sa.Column('modelLayout', sa.String(length=500), nullable=True))
    op.add_column('coasterrides', sa.Column('openDate', sa.String(length=40), nullable=True))
    op.add_column('coasterrides', sa.Column('status', sa.Integer(), nullable=True))
    op.add_column('coasterrides', sa.Column('statusDate', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('coasterrides', 'statusDate')
    op.drop_column('coasterrides', 'status')
    op.drop_column('coasterrides', 'openDate')
    op.drop_column('coasterrides', 'modelLayout')
    op.drop_column('coasterrides', 'modelCategory')
    op.drop_column('coasterrides', 'make')
    op.drop_column('coasterrides', 'configuration')
    op.drop_column('coasterrides', 'coasterType')
    op.drop_column('coasterrides', 'coasterOrRide')
    op.drop_column('coasterparks', 'statusDate')
    op.drop_column('coasterparks', 'status')
    op.drop_column('coasterparks', 'openDate')
    op.drop_column('coasterparks', 'address')
    # ### end Alembic commands ###
