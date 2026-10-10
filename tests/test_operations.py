import re
from sqlalchemy.exc import OperationalError
from app import crud


def test_every_response_carries_a_generated_request_id(client):
    r = client.get("/health")
    assert re.fullmatch(r"[0-9a-f]{32}", r.headers["X-Request-ID"])


def test_a_safe_client_request_id_is_echoed_back(client):
    r = client.get("/health", headers={"X-Request-ID": "trace-abc.123"})
    assert r.headers["X-Request-ID"] == "trace-abc.123"


def test_an_unsafe_client_request_id_is_replaced(client):
    r = client.get("/health", headers={"X-Request-ID": "a b;rm -rf"})
    assert re.fullmatch(r"[0-9a-f]{32}", r.headers["X-Request-ID"])


def test_database_outage_during_a_write_is_503_with_retry_after(client, monkeypatch):
    def boom(db, data):
        raise OperationalError("INSERT", {}, Exception("connection refused"))
    monkeypatch.setattr(crud, "create_author", boom)
    r = client.post("/authors/", json={"name": "Anyone"})
    assert r.status_code == 503
    assert r.headers["Retry-After"] == "5"
    assert r.json() == {"detail": "Database unavailable"}


def test_request_log_line_contains_status_and_request_id(client, caplog):
    import logging
    with caplog.at_level(logging.INFO, logger="catalog"):
        client.get("/health", headers={"X-Request-ID": "log-check-1"})
    assert any("GET /health -> 200" in m and "rid=log-check-1" in m for m in caplog.messages)
