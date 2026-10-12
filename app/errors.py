# """Translate database and domain failures into deliberate HTTP responses.

# The database is the final authority on integrity (PyVol 3). The API's job is to
# turn its refusals into errors a client can act on, instead of a bare 500.
# """
# import logging

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from sqlalchemy.exc import IntegrityError, OperationalError

# log = logging.getLogger("catalog")

# UNIQUE_MESSAGES = {
#     "uq_authors_name": "An author with that name already exists",
#     "uq_books_author_title": "This author already has a book with that title",
# }


# class DomainConflict(Exception):
#     """A valid request that conflicts with current state (HTTP 409)."""

#     def __init__(self, message: str):
#         self.message = message


# def _pg(exc: IntegrityError):
#     orig = exc.orig
#     return getattr(orig, "pgcode", None), getattr(getattr(orig, "diag", None), "constraint_name", None)


# def register_error_handlers(app: FastAPI) -> None:
#     @app.exception_handler(DomainConflict)
#     async def domain_conflict(request: Request, exc: DomainConflict):
#         return JSONResponse(status_code=409, content={"detail": exc.message})

#     @app.exception_handler(IntegrityError)
#     async def integrity_error(request: Request, exc: IntegrityError):
#         code, constraint = _pg(exc)
#         if code == "23505":  # unique_violation
#             msg = UNIQUE_MESSAGES.get(constraint, "Resource already exists")
#             return JSONResponse(status_code=409, content={"detail": msg})
#         if code == "23503":  # foreign_key_violation on write
#             return JSONResponse(status_code=422, content={"detail": [
#                 {"loc": ["body", "author_id"], "msg": "Author does not exist"}]})
#         if code == "23514":  # check_violation
#             return JSONResponse(status_code=422, content={"detail": [
#                 {"loc": ["body"], "msg": f"Value violates rule {constraint}"}]})
#         log.exception("Unmapped integrity error (pgcode=%s, constraint=%s)", code, constraint)
#         return JSONResponse(status_code=500, content={"detail": "Internal server error"})

#     @app.exception_handler(OperationalError)
#     async def database_unavailable(request: Request, exc: OperationalError):
#         # Connection refused, server restarting, network partition, timeout...
#         # The client did nothing wrong and may succeed later: 503, not 500.
#         log.error("Database unavailable: %s", exc.orig)
#         return JSONResponse(status_code=503, content={"detail": "Database unavailable"},
#                             headers={"Retry-After": "5"})





























import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError

import app

log = logging.getLogger("catalog_api")

uNIQUE_MESSAGE = {
    "access_message": "unique_message",
    "access_message2": "unique_message2"
}

class DomainConfig(Exception):
    def __ini__(self, message:str):
        self.message = message

def _pg(exc):
    ori = exc.ori

    return getattr(ori, "pg_code", None), getattr(getattr(ori, "diag", None), "constarint_name", None)

def registration_error_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainConfig)
    async def domain_config(request: Request, exc: DomainConfig):
        ret
