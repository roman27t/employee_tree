"""Update Staff unique_compound_key

Revision ID: f0ead9d3466e
Revises: 56ea4907a8f4
Create Date: 2022-12-03 13:57:07.608545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0ead9d3466e'
down_revision = '56ea4907a8f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff', sa.Column('birthdate', sa.Date(), nullable=False))
    op.create_unique_constraint('unique_compound_key', 'staff', ['last_name', 'birthdate', 'position_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_compound_key', 'staff', type_='unique')
    op.drop_column('staff', 'birthdate')
    # ### end Alembic commands ###
