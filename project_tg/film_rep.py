from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models import Film


class FilmRepository:
    """Репозиторий для работы с фильмами."""

    def __init__(self, database):
        self.database = database

    def save_film(
        self,
        tg_user_id: int,
        movie_id: int | None,
        movie_name: str,
        genre_name: str,
        rating_film: int = 0,
    ) -> Film:

        session = self.database.get_session()

        try:
            film = Film(
                tg_user_id=tg_user_id,
                movie_id=movie_id,
                movie_name=movie_name,
                genre_name=genre_name,
                rating_film=rating_film,
            )

            session.add(film)
            session.commit()
            session.refresh(film)

            return film

        except SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()

    def get_user_films(
        self,
        tg_user_id: int,
    ) -> list[Film]:

        session = self.database.get_session()

        try:
            query = (
                select(Film)
                .where(
                    Film.tg_user_id == tg_user_id
                )
                .order_by(
                    Film.watched_at.desc()
                )
            )

            return list(
                session.scalars(query).all()
            )

        except SQLAlchemyError:
            raise

        finally:
            session.close()

    def get_film(
        self,
        tg_user_id: int,
        film_id: int,
    ) -> Film | None:

        session = self.database.get_session()

        try:
            query = (
                select(Film)
                .where(
                    Film.id == film_id,
                    Film.tg_user_id == tg_user_id,
                )
            )

            return session.scalar(query)

        except SQLAlchemyError:
            raise

        finally:
            session.close()

    def update_review(
        self,
        tg_user_id: int,
        film_id: int,
        rating: int,
        note: str | None,
    ) -> bool:

        session = self.database.get_session()

        try:
            query = (
                select(Film)
                .where(
                    Film.id == film_id,
                    Film.tg_user_id == tg_user_id,
                )
            )

            film = session.scalar(query)

            if film is None:
                return False

            film.rating_film = rating
            film.note = note

            session.commit()

            return True

        except SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()