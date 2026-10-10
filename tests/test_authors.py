def test_create_author_returns_201_and_body(client):
    r = client.post("/authors/", json={"name": "Toni Morrison", "country": "USA"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "name": "Toni Morrison", "country": "USA"}


def test_country_is_optional(client):
    r = client.post("/authors/", json={"name": "Anonymous"})
    assert r.status_code == 201
    assert r.json()["country"] is None


def test_name_whitespace_is_stripped(client):
    r = client.post("/authors/", json={"name": "  Haruki Murakami  "})
    assert r.json()["name"] == "Haruki Murakami"


def test_blank_name_is_rejected(client):
    assert client.post("/authors/", json={"name": "   "}).status_code == 422


def test_missing_name_is_rejected(client):
    assert client.post("/authors/", json={"country": "Nigeria"}).status_code == 422


def test_duplicate_author_name_returns_409(client, author):
    r = client.post("/authors/", json={"name": author["name"]})
    assert r.status_code == 409


def test_get_author_and_404(client, author):
    assert client.get(f"/authors/{author['id']}").json()["name"] == "Chinua Achebe"
    assert client.get("/authors/9999").status_code == 404


def test_non_integer_author_id_is_422(client):
    assert client.get("/authors/abc").status_code == 422


def test_list_authors_paginates_with_total(client):
    for n in range(5):
        client.post("/authors/", json={"name": f"Author {n}"})
    page = client.get("/authors/", params={"limit": 2, "offset": 2}).json()
    assert page["total"] == 5
    assert [a["name"] for a in page["items"]] == ["Author 2", "Author 3"]


def test_delete_author_without_books_returns_204(client, author):
    assert client.delete(f"/authors/{author['id']}").status_code == 204
    assert client.get(f"/authors/{author['id']}").status_code == 404


def test_delete_author_with_books_returns_409(client, author, make_book):
    make_book()
    r = client.delete(f"/authors/{author['id']}")
    assert r.status_code == 409
    assert client.get(f"/authors/{author['id']}").status_code == 200


def test_unknown_query_parameter_on_author_list_is_422(client):
    assert client.get("/authors/", params={"limt": 5}).status_code == 422
