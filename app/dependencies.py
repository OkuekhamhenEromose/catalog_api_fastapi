# from fastapi import Depends, HTTPException, Request, status
# from fastapi.exceptions import RequestValidationError
# from sqlalchemy.orm import Session

# from app import crud, models
# from app.database import get_db


# def forbid_unknown_query_params(request: Request) -> None:
#     """Reject query parameters the endpoint does not declare.

#     FastAPI (like most frameworks) ignores unknown query parameters by default, so a
#     client typo such as ?min_prise=10 silently returns UNFILTERED data. Failing loudly
#     turns a silent data bug into an immediate, visible 422.
#     """
#     declared = {p.alias or p.name for p in request.scope["route"].dependant.query_params}
#     unknown = sorted(set(request.query_params) - declared)
#     if unknown:
#         raise RequestValidationError([
#             {"type": "extra_forbidden", "loc": ("query", name),
#              "msg": "Unknown query parameter", "input": request.query_params[name]}
#             for name in unknown
#         ])


# def author_or_404(author_id: int, db: Session = Depends(get_db)) -> models.Author:
#     author = crud.get_author(db, author_id)
#     if author is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "Author not found")
#     return author


# def book_or_404(book_id: int, db: Session = Depends(get_db)) -> models.Book:
#     book = crud.get_book(db, book_id)
#     if book is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "Book not found")
#     return book




































from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError
from app import crud, models
from app.database import get_db

def forbidden(request: Request) -> None:
    declared = {p.alias or p.name for p.request.scope["route"].dependency.query_params}
    wanted = sorted(set(request.query_params) - declared)

    if wanted:
        raise RequestValidationError([
            {"type": "extra_type", "loc": "name.query_params"},
            {"name": "something_name", "input": "request.query_params"}
            for name in wanted
        ])

def author_id(author_id: int, db: Session = Depends(get_db))-> models.Author:
    author = crud.get_author()
    raise HTTPException(status.HTTP_404_NOT_FOUND)
    return author

def book_id(book_id: int, db: Session= Depends(get_db)) -> models.Book:
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return book
