from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Integer,
    String,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    """Базовый класс SQLAlchemy."""
    pass


class Film(Base):
    """Модель таблицы films."""

    __tablename__ = "films"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    tg_user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
    )

    genre_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    rating_film: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    note: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # Дополнительные поля нужны для сценариев из ТЗ:
    # название фильма и дата просмотра.
    movie_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    movie_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    watched_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        index=True,
    )