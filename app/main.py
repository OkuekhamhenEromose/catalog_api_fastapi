import logging
import re
import time
import uuid

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import register_error_handlers
from app.routers import authors, books

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("catalog")

app = FastAPI(title="Book Catalog API", version="1.0.0")
register_error_handlers(app)
app.include_router(authors.router)
app.include_router(books.router)

SAFE_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{1,64}")


@app.middleware("http")
async def request_context(request: Request, call_next):
    """Give every request an ID, echo it back, and log one line per request."""
    supplied = request.headers.get("X-Request-ID", "")
    # Never trust a client-supplied value blindly: a newline in it would let a caller
    # forge log lines (log injection). Accept only a strict, short character set.
    request_id = supplied if SAFE_REQUEST_ID.fullmatch(supplied) else uuid.uuid4().hex
    started = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started) * 1000
    response.headers["X-Request-ID"] = request_id
    log.info("%s %s -> %s %.1fms rid=%s", request.method, request.url.path,
             response.status_code, elapsed_ms, request_id)
    return response


@app.get("/health", tags=["ops"])
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))  # proves the database is reachable, not just the process
    except SQLAlchemyError:
        # 503 tells load balancers "alive but not ready"; a bare 500 looks like a code bug.
        raise HTTPException(503, "Database unavailable")
    return {"status": "ok"}
