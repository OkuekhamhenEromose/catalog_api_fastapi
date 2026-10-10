from fastapi import Depends, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from app import crud, models
from app.database import get_db


def forbid_unknown_query_params(request: Request) -> None:
    """Reject query parameters the endpoint does not declare.

    FastAPI (like most frameworks) ignores unknown query parameters by default, so a
    client typo such as ?min_prise=10 silently returns UNFILTERED data. Failing loudly
    turns a silent data bug into an immediate, visible 422.
    """
    declared = {p.alias or p.name for p in request.scope["route"].dependant.query_params}
    unknown = sorted(set(request.query_params) - declared)
    if unknown:
        raise RequestValidationError([
            {"type": "extra_forbidden", "loc": ("query", name),
             "msg": "Unknown query parameter", "input": request.query_params[name]}
            for name in unknown
        ])


def author_or_404(author_id: int, db: Session = Depends(get_db)) -> models.Author:
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Author not found")
    return author


def book_or_404(book_id: int, db: Session = Depends(get_db)) -> models.Book:
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
    return book
