"""Add role and location to users table

Revision ID: 8c541c35a10a
Revises: 
Create Date: 2024-12-30 14:06:21.652945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c541c35a10a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

