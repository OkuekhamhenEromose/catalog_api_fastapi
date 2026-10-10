"""PyVol 3 lesson applied: the database refuses bad data even if the API is bypassed."""
import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from app.database import engine


def test_database_rejects_negative_price_directly():
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO authors (name) VALUES ('A')"))
    with pytest.raises(IntegrityError, match="ck_books_price_nonnegative"):
        with engine.begin() as conn:
            conn.execute(text(
                "INSERT INTO books (title, author_id, price) VALUES ('x', 1, -1)"))


def test_database_rejects_orphan_book_directly():
    with pytest.raises(IntegrityError, match="books_author_id_fkey"):
        with engine.begin() as conn:
            conn.execute(text(
                "INSERT INTO books (title, author_id, price) VALUES ('x', 999, 1)"))
