from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models
import schemas


def create_author(
    db: Session,
    author: schemas.AuthorCreate,
):
    db_author = models.Author(**author.model_dump())

    db.add(db_author)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_author)

    return db_author


def get_author(
    db: Session,
    author_id: int,
):
    return db.get(models.Author, author_id)


def get_authors(
    db: Session,
    skip: int = 0,
    limit: int = 10,
):
    statement = (
        select(models.Author)
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def create_book(
    db: Session,
    book: schemas.BookCreate,
    author_id: int,
):
    author = get_author(db, author_id)
    if author is None:
        return None

    db_book = models.Book(
        **book.model_dump(),
        author_id=author_id,
    )

    db.add(db_book)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_book)

    return db_book


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    author_id: int | None = None
):
    statement = select(models.Book)

    if author_id is not None:
        statement = statement.where(
            models.Book.author_id == author_id
        )

    statement = (
        statement
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()
