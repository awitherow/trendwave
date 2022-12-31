"""create tweets table

Revision ID: 930a08db1445
Revises: 
Create Date: 2022-12-31 10:27:33.761215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930a08db1445'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('tweets',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('text', sa.String),
                    sa.Column('approved', sa.Boolean)
                    )


def downgrade() -> None:
    op.drop_table('tweets')
