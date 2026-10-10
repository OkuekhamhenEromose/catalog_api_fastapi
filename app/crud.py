from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models, schemas
from app.errors import DomainConflict


# ---- authors -------------------------------------------------------------
def create_author(db: Session, data: schemas.AuthorCreate) -> models.Author:
    author = models.Author(**data.model_dump())
    db.add(author)
    db.commit()
    return author


def get_author(db: Session, author_id: int) -> models.Author | None:
    return db.get(models.Author, author_id)


def list_authors(db: Session, limit: int, offset: int):
    total = db.scalar(select(func.count()).select_from(models.Author))
    stmt = select(models.Author).order_by(models.Author.id).limit(limit).offset(offset)
    return list(db.scalars(stmt)), total


def delete_author(db: Session, author: models.Author) -> None:
    try:
        db.delete(author)
        db.commit()
    except IntegrityError:  # ON DELETE RESTRICT: the author still owns books
        db.rollback()
        raise DomainConflict("Author still has books; delete or move them first")


# ---- books ---------------------------------------------------------------
def create_book(db: Session, data: schemas.BookCreate) -> models.Book:
    book = models.Book(**data.model_dump())
    db.add(book)
    db.commit()
    return book


def get_book(db: Session, book_id: int) -> models.Book | None:
    return db.get(models.Book, book_id)


def update_book(db: Session, book: models.Book, changes: dict) -> models.Book:
    for field, value in changes.items():
        setattr(book, field, value)
    db.commit()
    return book


def delete_book(db: Session, book: models.Book) -> None:
    db.delete(book)
    db.commit()


# ---- book listing --------------------------------------------------------
SORT_COLUMNS = {
    "id": models.Book.id,
    "title": models.Book.title,
    "price": models.Book.price,
    "created_at": models.Book.created_at,
}


def _escape_like(text_: str) -> str:
    """Make %, _ and \\ in user input match literally inside ILIKE."""
    return text_.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def list_books(db: Session, *, author_id, in_stock, min_price, max_price, q, sort, limit, offset):
    B = models.Book
    conditions = []
    if author_id is not None:
        conditions.append(B.author_id == author_id)
    if in_stock is not None:
        conditions.append(B.in_stock == in_stock)
    if min_price is not None:
        conditions.append(B.price >= min_price)
    if max_price is not None:
        conditions.append(B.price <= max_price)
    if q:
        conditions.append(B.title.ilike(f"%{_escape_like(q)}%", escape="\\"))

    total = db.scalar(select(func.count()).select_from(B).where(*conditions))
    column = SORT_COLUMNS[sort.lstrip("-")]
    primary = column.desc() if sort.startswith("-") else column.asc()
    # B.id as a final tiebreaker makes pages deterministic: without it, rows with equal
    # sort keys may appear on two pages or on none while the client paginates.
    stmt = select(B).where(*conditions).order_by(primary, B.id).limit(limit).offset(offset)
    return list(db.scalars(stmt)), total
