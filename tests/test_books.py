def test_create_book_returns_201_with_numeric_price(make_book):
    r = make_book()
    assert r.status_code == 201
    body = r.json()
    assert body["price"] == 12.99          # a JSON number, not the string "12.99"
    assert body["in_stock"] is True         # server-side default applied
    assert body["id"] == 1


def test_create_book_for_missing_author_returns_422(client):
    r = client.post("/books/", json={"title": "Orphan", "author_id": 999, "price": 10})
    assert r.status_code == 422
    assert r.json()["detail"][0]["msg"] == "Author does not exist"


def test_negative_price_is_rejected(make_book):
    assert make_book(price=-5).status_code == 422


def test_price_with_three_decimals_is_rejected(make_book):
    assert make_book(price=1.999).status_code == 422


def test_price_too_large_for_column_is_rejected(make_book):
    assert make_book(price=10000).status_code == 422


def test_missing_title_is_rejected(client, author):
    r = client.post("/books/", json={"author_id": author["id"], "price": 5})
    assert r.status_code == 422


def test_unknown_field_is_rejected(make_book):
    assert make_book(colour="red").status_code == 422


def test_same_title_for_same_author_returns_409(make_book):
    assert make_book().status_code == 201
    assert make_book().status_code == 409


def test_same_title_for_different_author_is_allowed(client, make_book):
    make_book()
    other = client.post("/authors/", json={"name": "Someone Else"}).json()
    assert make_book(author_id=other["id"]).status_code == 201


def test_get_book_and_404(client, make_book):
    book = make_book().json()
    assert client.get(f"/books/{book['id']}").json()["title"] == "Things Fall Apart"
    assert client.get("/books/9999").status_code == 404


def test_patch_price_only_leaves_other_fields_alone(client, make_book):
    book = make_book().json()
    r = client.patch(f"/books/{book['id']}", json={"price": 14.5})
    assert r.status_code == 200
    assert r.json()["price"] == 14.5
    assert r.json()["title"] == "Things Fall Apart"


def test_patch_can_set_in_stock_false(client, make_book):
    book = make_book().json()
    r = client.patch(f"/books/{book['id']}", json={"in_stock": False})
    assert r.json()["in_stock"] is False


def test_patch_null_title_is_rejected_not_a_500(client, make_book):
    book = make_book().json()
    r = client.patch(f"/books/{book['id']}", json={"title": None})
    assert r.status_code == 422


def test_patch_empty_body_is_rejected(client, make_book):
    book = make_book().json()
    assert client.patch(f"/books/{book['id']}", json={}).status_code == 422


def test_patch_cannot_change_author(client, make_book):
    book = make_book().json()
    assert client.patch(f"/books/{book['id']}", json={"author_id": 2}).status_code == 422


def test_patch_missing_book_returns_404(client):
    assert client.patch("/books/9999", json={"price": 1}).status_code == 404


def test_patch_to_duplicate_title_returns_409(client, author, make_book):
    make_book(title="A")
    b = make_book(title="B").json()
    assert client.patch(f"/books/{b['id']}", json={"title": "A"}).status_code == 409


def test_delete_book_then_404(client, make_book):
    book = make_book().json()
    assert client.delete(f"/books/{book['id']}").status_code == 204
    assert client.get(f"/books/{book['id']}").status_code == 404
    assert client.delete(f"/books/{book['id']}").status_code == 404
