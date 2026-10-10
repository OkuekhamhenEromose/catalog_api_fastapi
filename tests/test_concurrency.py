"""Edge case: N identical requests arrive at the same moment.

A check-then-insert in application code would let several through. The UNIQUE
constraint (PyVol 3) is evaluated atomically inside PostgreSQL, so exactly one wins.
"""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor


def test_simultaneous_duplicate_author_creates_yield_exactly_one_winner(client):
    def create(_):
        return client.post("/authors/", json={"name": "Race Condition"}).status_code

    with ThreadPoolExecutor(max_workers=12) as pool:
        statuses = list(pool.map(create, range(12)))

    assert Counter(statuses) == {201: 1, 409: 11}
    assert client.get("/authors/").json()["total"] == 1


def test_simultaneous_duplicate_book_creates_yield_exactly_one_winner(client, author):
    payload = {"title": "One Copy Only", "author_id": author["id"], "price": 9.5}

    def create(_):
        return client.post("/books/", json=payload).status_code

    with ThreadPoolExecutor(max_workers=12) as pool:
        statuses = list(pool.map(create, range(12)))

    assert Counter(statuses) == {201: 1, 409: 11}
