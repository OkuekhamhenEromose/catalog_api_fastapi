"""add indexes for the list endpoint's real query patterns

Revision ID: 0002
Revises: 0001
"""
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pg_trgm powers fast substring search (ILIKE '%term%'), which a normal B-tree cannot.
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    # Equality column first (in_stock), then the range/sort column (price), then id as the
    # tiebreaker used by ORDER BY price, id.
    op.create_index("ix_books_in_stock_price_id", "books", ["in_stock", "price", "id"])
    op.execute("CREATE INDEX ix_books_title_trgm ON books USING gin (title gin_trgm_ops)")


def downgrade() -> None:
    op.execute("DROP INDEX ix_books_title_trgm")
    op.drop_index("ix_books_in_stock_price_id", table_name="books")
