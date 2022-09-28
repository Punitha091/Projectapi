"""add_colum_to_sample

Revision ID: 07a7cb165fbd
Revises: c4b782f08a73
Create Date: 2022-09-27 14:51:03.900688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07a7cb165fbd'
down_revision = 'c4b782f08a73'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("sample" ,
    sa.Column("Address",sa.String , nullable = True))
    pass


def downgrade() -> None:
    op.drop_column("sample","Address")
    pass
