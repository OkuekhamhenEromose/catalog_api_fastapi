"""Regression guard: performance work is part of the schema, so test that it exists."""
from sqlalchemy import text
from app.database import engine


def test_query_pattern_indexes_exist():
    with engine.connect() as conn:
        names = {r[0] for r in conn.execute(
            text("SELECT indexname FROM pg_indexes WHERE tablename = 'books'"))}
    assert {"ix_books_in_stock_price_id", "ix_books_title_trgm",
            "uq_books_author_title"} <= names


def test_author_lookup_uses_the_unique_constraint_index_not_a_seq_scan():
    with engine.begin() as conn:
        conn.execute(text("SET LOCAL enable_seqscan = off"))
        plan = "\n".join(r[0] for r in conn.execute(
            text("EXPLAIN SELECT id FROM books WHERE author_id = 1")))
    assert "uq_books_author_title" in plan
