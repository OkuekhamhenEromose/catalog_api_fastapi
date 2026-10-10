from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.dependencies import book_or_404, forbid_unknown_query_params

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(data: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, data)


SortField = Literal["id", "-id", "title", "-title", "price", "-price",
                    "created_at", "-created_at"]


@router.get("/", response_model=schemas.BookPage, dependencies=[Depends(forbid_unknown_query_params)])
def list_books(
    author_id: int | None = Query(None, gt=0),
    in_stock: bool | None = None,
    min_price: Decimal | None = Query(None, ge=0),
    max_price: Decimal | None = Query(None, ge=0),
    q: str | None = Query(None, min_length=1, max_length=100),
    sort: SortField = "id",
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(422, "min_price cannot be greater than max_price")
    items, total = crud.list_books(
        db, author_id=author_id, in_stock=in_stock, min_price=min_price,
        max_price=max_price, q=q, sort=sort, limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{book_id}", response_model=schemas.BookRead)
def get_book(book: models.Book = Depends(book_or_404)):
    return book


@router.patch("/{book_id}", response_model=schemas.BookRead)
def update_book(data: schemas.BookUpdate, book: models.Book = Depends(book_or_404),
                db: Session = Depends(get_db)):
    return crud.update_book(db, book, data.model_dump(exclude_unset=True))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book: models.Book = Depends(book_or_404), db: Session = Depends(get_db)):
    crud.delete_book(db, book)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
