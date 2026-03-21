"""create drivers table from sql

Revision ID: 4e4c227bb3e3
Revises: 3b35b650c1a1
Create Date: 2025-09-10 13:54:05.912396

"""
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e4c227bb3e3'
down_revision: Union[str, None] = '3b35b650c1a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SQL_PATH = Path(__file__).resolve().parents[1] / "sql" / "001_create_drivers_table.sql"


def upgrade() -> None:
    sql = SQL_PATH.read_text(encoding="utf-8")
    op.execute(sql)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS drivers;")
