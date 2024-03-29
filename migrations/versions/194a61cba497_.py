"""empty message

Revision ID: 194a61cba497
Revises: fe5c567d96bd
Create Date: 2024-02-18 17:18:43.668557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194a61cba497'
down_revision = 'fe5c567d96bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('district',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.Enum('PITSEA', 'LAINDON', 'VANGE', 'FRYERNS', 'CRAYLANDS', 'BARSTABLE', 'KINGSWOOD', 'GHYLLGROVE', 'LEE_CHAPEL_SOUTH', 'LEE_CHAPEL_NORTH', 'LANGDON_HILLS', 'DRY_STREET', 'GREAT_BERRY', 'NOAK_BRIDGE', 'STEEPLE_VIEW', 'PIPPS_HILL', 'CRANES', name='district'),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('district',
               existing_type=sa.Enum('PITSEA', 'LAINDON', 'VANGE', 'FRYERNS', 'CRAYLANDS', 'BARSTABLE', 'KINGSWOOD', 'GHYLLGROVE', 'LEE_CHAPEL_SOUTH', 'LEE_CHAPEL_NORTH', 'LANGDON_HILLS', 'DRY_STREET', 'GREAT_BERRY', 'NOAK_BRIDGE', 'STEEPLE_VIEW', 'PIPPS_HILL', 'CRANES', name='district'),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###
