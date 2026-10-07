from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column(String(500))

    books: Mapped[list["Book"]] = relationship(
        back_populates="author"
    )


class Book(Base):
    __tablename__ = "books"

    __table_args__ = (
        UniqueConstraint("title", name="uq_books_title"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    summary: Mapped[str]
    publication_date: Mapped[date]

    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id")
    )

    author: Mapped["Author"] = relationship(
        back_populates="books"
    )
