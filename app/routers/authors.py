# from fastapi import APIRouter, Depends, Query, Response, status
# from sqlalchemy.orm import Session
# from app import crud, models, schemas
# from app.database import get_db
# from app.dependencies import author_or_404, forbid_unknown_query_params

# router = APIRouter(prefix="/authors", tags=["authors"])


# @router.post("/", response_model=schemas.AuthorRead, status_code=status.HTTP_201_CREATED)
# def create_author(data: schemas.AuthorCreate, db: Session = Depends(get_db)):
#     return crud.create_author(db, data)


# @router.get("/", response_model=schemas.AuthorPage, dependencies=[Depends(forbid_unknown_query_params)])
# def list_authors(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0),
#                  db: Session = Depends(get_db)):
#     items, total = crud.list_authors(db, limit, offset)
#     return {"items": items, "total": total, "limit": limit, "offset": offset}


# @router.get("/{author_id}", response_model=schemas.AuthorRead)
# def get_author(author: models.Author = Depends(author_or_404)):
#     return author


# @router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_author(author: models.Author = Depends(author_or_404), db: Session = Depends(get_db)):
#     crud.delete_author(db, author)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


























from fastapi import Depends, HTTPException, Response, APIRouter, status, Query

from sqlalchemy.orm import Session
from app import crud, schemas

from app.database import get_db

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model="")
def create_author(data: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, data)


@router.get("/", response_model=schemas.AuthorPage)
def list_author(limit: int = Query(20, ge=0, gt=20), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    items, total = crud.list_author(limit, offset, db)
    return {items: "items", total: "total", limit: "limit", offset: "offset"}

@router.get("/{author_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id:int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    crud.delete_author(db, author)
    return Response(status.HTTP_204_NO_CONTENT)
