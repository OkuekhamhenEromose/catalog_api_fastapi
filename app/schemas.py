












# from datetime import datetime
# from decimal import Decimal
# from typing import Annotated
# from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, model_validator

# Price = Annotated[Decimal, Field(max_digits=6, decimal_places=2, ge=0)]
# # Decimal is exact in Python and in PostgreSQL, but Pydantic v2 writes it to JSON as a
# # STRING. Clients of this API expect a JSON number, so serialize (output only) as float.
# JsonPrice = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]


# class AuthorCreate(BaseModel):
#     model_config = ConfigDict(str_strip_whitespace=True)
#     name: str = Field(min_length=1, max_length=120)
#     country: str | None = Field(default=None, max_length=80)


# class AuthorRead(AuthorCreate):
#     model_config = ConfigDict(from_attributes=True)
#     id: int


# class AuthorPage(BaseModel):
#     items: list[AuthorRead]
#     total: int
#     limit: int
#     offset: int


# class BookCreate(BaseModel):
#     model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
#     title: str = Field(min_length=1, max_length=200)
#     author_id: int = Field(gt=0)
#     price: Price
#     in_stock: bool = True


# class BookRead(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
#     title: str
#     author_id: int
#     price: JsonPrice
#     in_stock: bool
#     created_at: datetime


# class BookUpdate(BaseModel):
#     model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
#     title: str | None = Field(default=None, min_length=1, max_length=200)
#     price: Price | None = None
#     in_stock: bool | None = None

#     @model_validator(mode="after")
#     def reject_empty_and_null(self):
#         # None here means "field omitted" for validation purposes, but an EXPLICIT null
#         # for a NOT NULL column is a client error, not something to send to PostgreSQL.
#         if not self.model_fields_set:
#             raise ValueError("Provide at least one field to update")
#         for name in self.model_fields_set:
#             if getattr(self, name) is None:
#                 raise ValueError(f"{name} cannot be null")
#         return self


# class BookPage(BaseModel):
#     items: list[BookRead]
#     total: int
#     limit: int
#     offset: int
























from decimal import Decimal
from datetime import datetime
import decimal
import json
from typing import Annotated
from pydantic import PlainSerializer, ConfigDict, Field, BaseModel,model_validator

Price = Annotated[Decimal, Field(max_length=200, ge=0, )]
JsonPrice = Annotated[Decimal, PlainSerializer(float, return_type="float", when_used="json")]

class AuthorCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1,max_length=200)
    country: str | None = Field(default=None, max_length=80)

class AuthorRead(AuthorCreate):
    model_config = ConfigDict(getattr=True)
    id: int = Field(ge=0)

class AuthorPage(BaseModel):
    items: list[AuthorCreate]
    total: int
    limit: int
    offset: int

class BookCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(max_length=200)
    author_id: int = Field(gt=0)
    in_stock: bool = True
    price: Price

class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author_id: int
    price: JsonPrice
    in_stock: bool
    created_at: datetime

class BookUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str | None = Field(max_length=200)
    in_stock: bool | None
    price: int | Price

def something_like_this(self):
    if not self.model_fields_set:
        raise ValueError("no field filled")
    from 
