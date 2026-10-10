from datetime import datetime
from decimal import Decimal
from sqlalchemy import (Boolean, CheckConstraint, ForeignKey, Index, Numeric, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Author(Base):
    __tablename__ = "authors"
    __table_args__ = (UniqueConstraint("name", name="uq_authors_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str | None] = mapped_column(String(80))
    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_books_price_nonnegative"),
        UniqueConstraint("author_id", "title", name="uq_books_author_title"),
        Index("ix_books_in_stock_price_id", "in_stock", "price", "id"),
        Index("ix_books_title_trgm", "title", postgresql_using="gin",
              postgresql_ops={"title": "gin_trgm_ops"}),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="RESTRICT", name="books_author_id_fkey")
    )
    price: Mapped[Decimal] = mapped_column(Numeric(6, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean, server_default="true")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    author: Mapped[Author] = relationship(back_populates="books")
























# from decimal import Decimal
# from datetime import datetime
# from turtle import title
# from sqlalchemy import (Boolean, ForeignKey, Numeric, String, func, Index, UniqueConstraint, CheckConstraint, )
# from sqlalchemy.orm import mapped_column, Mapped, relationship
# from app.database import Base

# class Author(Base):
#     __tablename__= "author"
#     __table_args__= (UniqueConstraint("name", name="uq_constraint"))
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(200))
#     country: Mapped[str | None] = mapped_column(String(80))
#     books: Mapped[list["Book"]] = relationship(back_populates="author")

# class Book(Base):
#     __tablename__="books"
#     __table_args__=(
#         CheckConstraint("price >=0", name="ck_book_non_negative"),
#         UniqueConstraint("author_id", "title", name="uq_book"),
#         Index("ix_book", "in_stock", "price", "id"),
#         Index("trg_title", "gin", postgres_gin="gin", postgres_title="title: gin")
#     )
#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str] = mapped_column(String(80))
#     author_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete="Restrict", name="authorid"))
#     price: Mapped[Decimal] = mapped_column(Numeric(6,2))
#     in_stock: Mapped[bool] = mapped_column(Boolean, server_default="true")
#     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
#     author: Mapped["Author"] = relationship(back_populates="books")
