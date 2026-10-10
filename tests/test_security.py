"""Security controls, each proven by an attack that fails."""
from sqlalchemy import text
from app.database import engine


def test_sql_injection_in_search_is_treated_as_plain_text(client, author, make_book):
    make_book()
    attack = "'; DROP TABLE books; --"
    r = client.get("/books/", params={"q": attack})
    assert r.status_code == 200 and r.json()["items"] == []
    with engine.connect() as conn:  # the table must still exist and still hold our row
        assert conn.execute(text("SELECT count(*) FROM books")).scalar() == 1


def test_sql_injection_in_sort_is_blocked_by_allowlist(client):
    r = client.get("/books/", params={"sort": "id; DROP TABLE books"})
    assert r.status_code == 422


def test_quotes_in_titles_are_stored_literally(client, make_book):
    r = make_book(title="Robert'); DROP TABLE books;--")
    assert r.status_code == 201
    assert r.json()["title"] == "Robert'); DROP TABLE books;--"


def test_mass_assignment_of_server_owned_fields_is_rejected(client, author):
    r = client.post("/books/", json={"title": "X", "author_id": author["id"], "price": 1,
                                     "id": 999, "created_at": "1999-01-01T00:00:00"})
    assert r.status_code == 422


def test_pagination_cap_prevents_unbounded_responses(client):
    assert client.get("/books/", params={"limit": 100000}).status_code == 422


def test_unhandled_errors_do_not_leak_internals(client, monkeypatch):
    from app import crud

    def boom(*a, **k):
        raise RuntimeError("secret connection string postgresql://user:pw@host/db")
    monkeypatch.setattr(crud, "create_author", boom)
    r = client.post("/authors/", json={"name": "Anyone"})
    assert r.status_code == 500
    assert "postgresql://" not in r.text and "secret" not in r.text
