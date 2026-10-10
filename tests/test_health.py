def test_health_reports_ok_and_touches_database(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_health_returns_503_when_database_is_down(client):
    from sqlalchemy.exc import OperationalError
    from app.database import get_db
    from app.main import app

    class BrokenSession:
        def execute(self, *a, **k):
            raise OperationalError("SELECT 1", {}, Exception("connection refused"))

    app.dependency_overrides[get_db] = lambda: BrokenSession()
    try:
        r = client.get("/health")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 503
    assert r.json() == {"detail": "Database unavailable"}
