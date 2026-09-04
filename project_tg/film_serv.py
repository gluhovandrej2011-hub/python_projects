class FilmService:
    """Основная бизнес-логика FilmWatcher."""

    def __init__(
        self,
        repository,
        ninjas_api,
    ):
        self.repository = repository
        self.ninjas_api = ninjas_api

    def get_popular_movies(self):
        """Возвращает 3 самых популярных фильма."""

        return (
            self.ninjas_api
            .get_popular_movies()
        )

    def search_movies(
        self,
        genre: str,
        min_rating: float,
    ):
        """Возвращает максимум 5 фильмов."""

        return (
            self.ninjas_api
            .find_by_genre_and_rating(
                genre,
                min_rating,
            )
        )

    def save_selected_movie(
        self,
        tg_user_id: int,
        movie: dict,
        genre: str,
    ):

        movie_id = movie.get("id")

        movie_name = (
            movie.get("title")
            or movie.get("name")
            or "Без названия"
        )

        # 0 означает, что пользователь
        # пока не поставил собственную оценку.
        return self.repository.save_film(
            tg_user_id=tg_user_id,
            movie_id=movie_id,
            movie_name=movie_name,
            genre_name=genre,
            rating_film=0,
        )

    def get_history(
        self,
        tg_user_id: int,
    ):
        return self.repository.get_user_films(
            tg_user_id
        )

    def get_history_film(
        self,
        tg_user_id: int,
        film_id: int,
    ):
        return self.repository.get_film(
            tg_user_id,
            film_id,
        )

    def add_review(
        self,
        tg_user_id: int,
        film_id: int,
        rating: int,
        note: str | None,
    ):

        return self.repository.update_review(
            tg_user_id=tg_user_id,
            film_id=film_id,
            rating=rating,
            note=note,
        )