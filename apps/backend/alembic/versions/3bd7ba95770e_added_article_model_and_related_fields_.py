"""added Article model and related fields to other models

Revision ID: 3bd7ba95770e
Revises: cbfeae7b52f1
Create Date: 2025-03-08 20:19:05.338535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bd7ba95770e'
down_revision: Union[str, None] = 'cbfeae7b52f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
