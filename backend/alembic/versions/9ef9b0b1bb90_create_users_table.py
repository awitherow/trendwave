"""create users table

Revision ID: 9ef9b0b1bb90
Revises: 930a08db1445
Create Date: 2023-01-01 11:50:28.268542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ef9b0b1bb90'
down_revision = '930a08db1445'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True),
        sa.Column("password", sa.String)
    )


def downgrade():
    op.drop_table("users")
