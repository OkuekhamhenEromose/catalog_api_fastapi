import pytest


@pytest.fixture
def catalog(client):
    """Two authors, six books with known titles, prices and stock."""
    a = client.post("/authors/", json={"name": "Chinua Achebe", "country": "Nigeria"}).json()
    b = client.post("/authors/", json={"name": "Toni Morrison"}).json()
    rows = [
        ("Things Fall Apart", a["id"], 12.99, True),
        ("No Longer at Ease", a["id"], 10.50, True),
        ("Beloved", b["id"], 15.00, True),
        ("Song of Solomon", b["id"], 13.25, False),
        ("Sula", b["id"], 9.00, True),
        ("100% Pure Fiction", b["id"], 20.00, True),
    ]
    for title, author_id, price, stock in rows:
        r = client.post("/books/", json={"title": title, "author_id": author_id,
                                         "price": price, "in_stock": stock})
        assert r.status_code == 201, r.text
    return {"achebe": a["id"], "morrison": b["id"]}


def titles(response):
    return [b["title"] for b in response.json()["items"]]


def test_default_listing_returns_everything_with_total(client, catalog):
    body = client.get("/books/").json()
    assert body["total"] == 6 and len(body["items"]) == 6
    assert (body["limit"], body["offset"]) == (20, 0)


def test_filter_by_author(client, catalog):
    r = client.get("/books/", params={"author_id": catalog["achebe"]})
    assert sorted(titles(r)) == ["No Longer at Ease", "Things Fall Apart"]


def test_filter_in_stock_false(client, catalog):
    assert titles(client.get("/books/", params={"in_stock": False})) == ["Song of Solomon"]


def test_filter_price_range_is_inclusive(client, catalog):
    r = client.get("/books/", params={"min_price": 10.50, "max_price": 13.25, "sort": "price"})
    assert titles(r) == ["No Longer at Ease", "Things Fall Apart", "Song of Solomon"]


def test_search_is_case_insensitive_substring(client, catalog):
    assert titles(client.get("/books/", params={"q": "fall"})) == ["Things Fall Apart"]


def test_search_treats_percent_literally(client, catalog):
    # An unescaped '%' would match every title; escaped, only "100% Pure Fiction".
    assert titles(client.get("/books/", params={"q": "100%"})) == ["100% Pure Fiction"]


def test_filters_combine_with_and(client, catalog):
    r = client.get("/books/", params={"author_id": catalog["morrison"], "in_stock": True,
                                      "max_price": 15, "sort": "-price"})
    assert titles(r) == ["Beloved", "Sula"]


def test_sort_by_price_descending(client, catalog):
    assert titles(client.get("/books/", params={"sort": "-price"}))[0] == "100% Pure Fiction"


def test_total_ignores_limit_and_offset(client, catalog):
    body = client.get("/books/", params={"limit": 2, "offset": 4}).json()
    assert body["total"] == 6 and len(body["items"]) == 2


def test_pages_do_not_overlap_or_skip(client, catalog):
    seen = []
    for offset in (0, 2, 4):
        seen += titles(client.get("/books/", params={"limit": 2, "offset": offset}))
    assert len(seen) == len(set(seen)) == 6


def test_offset_past_the_end_returns_empty_items(client, catalog):
    body = client.get("/books/", params={"offset": 100}).json()
    assert body["items"] == [] and body["total"] == 6


@pytest.mark.parametrize("params", [
    {"limit": 0}, {"limit": 101}, {"offset": -1}, {"min_price": -1},
    {"sort": "author"}, {"sort": "price; DROP TABLE books"}, {"in_stock": "maybe"},
    {"author_id": 0}, {"min_price": "abc"},
])


def test_invalid_query_values_are_422(client, catalog, params):
    assert client.get("/books/", params=params).status_code == 422


def test_min_price_above_max_price_is_422(client, catalog):
    assert client.get("/books/", params={"min_price": 20, "max_price": 5}).status_code == 422


def test_unknown_query_parameter_is_rejected_not_ignored(client, catalog):
    # A typo like 'min_prise' must not silently return the unfiltered catalog.
    r = client.get("/books/", params={"min_prise": 10})
    assert r.status_code == 422
    assert "min_prise" in str(r.json())
