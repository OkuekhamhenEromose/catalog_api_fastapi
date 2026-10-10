import os

# Must be set BEFORE importing the app: the engine is built at import time.
os.environ["DATABASE_URL"] = (
    "postgresql+psycopg2://course_user:course_pass@localhost/catalog_test"
)

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def migrated_database():
    """Build the test schema from the REAL migrations, not from create_all()."""
    cfg = Config("alembic.ini")
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    yield


@pytest.fixture(autouse=True)
def clean_tables():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE books, authors RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
def client():
    # raise_server_exceptions=False: behave like production, where an unhandled
    # exception becomes an HTTP 500 instead of crashing the caller.
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


@pytest.fixture
def author(client):
    r = client.post("/authors/", json={"name": "Chinua Achebe", "country": "Nigeria"})
    assert r.status_code == 201, r.text
    return r.json()


@pytest.fixture
def make_book(client, author):
    def _make(**overrides):
        payload = {"title": "Things Fall Apart", "author_id": author["id"], "price": 12.99}
        payload.update(overrides)
        return client.post("/books/", json=payload)
    return _make
