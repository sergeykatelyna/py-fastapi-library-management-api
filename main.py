from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import Base, SessionLocal, engine
import schemas
import crud
import models   # noqa: F401


app = FastAPI()


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/authors", response_model=schemas.AuthorRead)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db),
):
    try:
        new_author = crud.create_author(db=db, author=author)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Author with this name already exists",
        )

    return new_author


@app.get("/authors", response_model=list[schemas.AuthorRead])
def get_authors(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@app.get("/authros/{author_id}", response_model=schemas.AuthorRead)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    author = crud.get_author(db=db, author_id=author_id)

    if author is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return author


@app.post(
    "/authors/{author_id}/books",
    response_model=schemas.BookRead,
)
def create_book(
    author_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
):
    try:
        new_book = crud.create_book(db=db, book=book, author_id=author_id)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Book with this title already exists",
        )

    if new_book is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return new_book


@app.get("/books", response_model=list[schemas.BookRead])
def get_books(
    author_id: int | None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    books = crud.get_books(db=db, skip=skip, limit=limit, author_id=author_id)

    if author_id is not None and books is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found",
        )

    return books
