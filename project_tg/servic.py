import requests


class NinjasAPIError(Exception):
    """Ошибка взаимодействия с API Ninjas."""


class NinjasAPI:
    """Клиент API Ninjas."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
    ):
        self.api_key = api_key
        self.base_url = base_url

    def _request(
        self,
        params: dict,
    ) -> list[dict]:

        headers = {
            "X-Api-Key": self.api_key,
        }

        try:
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10,
            )

            if response.status_code == 401:
                raise NinjasAPIError(
                    "Неверный API-ключ API Ninjas."
                )

            if response.status_code == 403:
                raise NinjasAPIError(
                    "Нет доступа к API Ninjas."
                )

            if response.status_code == 429:
                raise NinjasAPIError(
                    "Превышен лимит запросов API Ninjas."
                )

            response.raise_for_status()

            data = response.json()

            if isinstance(data, list):
                return data

            # Некоторые API возвращают объект,
            # внутри которого лежит список результатов.
            if isinstance(data, dict):

                for key in (
                    "movies",
                    "results",
                    "data",
                ):
                    if isinstance(
                        data.get(key),
                        list,
                    ):
                        return data[key]

            raise NinjasAPIError(
                "API вернул неожиданный формат данных."
            )

        except NinjasAPIError:
            raise

        except requests.Timeout as error:
            raise NinjasAPIError(
                "API Ninjas слишком долго отвечает."
            ) from error

        except requests.ConnectionError as error:
            raise NinjasAPIError(
                "Не удалось подключиться к API Ninjas."
            ) from error

        except requests.RequestException as error:
            raise NinjasAPIError(
                "Ошибка HTTP при обращении к API Ninjas."
            ) from error

        except ValueError as error:
            raise NinjasAPIError(
                "API Ninjas вернул некорректный JSON."
            ) from error

    @staticmethod
    def _rating(movie: dict) -> float:

        value = (
            movie.get("rating")
            or movie.get("imdb_rating")
            or movie.get("imdbRating")
            or 0
        )

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _title(movie: dict) -> str:

        return (
            movie.get("title")
            or movie.get("name")
            or "Без названия"
        )

    def get_popular_movies(self) -> list[dict]:
        """
        Получает фильмы и возвращает
        3 лучших по рейтингу.
        """

        movies = self._request({})

        movies.sort(
            key=self._rating,
            reverse=True,
        )

        return movies[:3]

    def search_movies(
        self,
        genre: str,
    ) -> list[dict]:
        """Ищет фильмы по жанру."""

        params = {
            "query": genre,
        }

        return self._request(params)

    def find_by_genre_and_rating(
        self,
        genre: str,
        min_rating: float,
    ) -> list[dict]:

        movies = self.search_movies(
            genre
        )

        filtered = [
            movie
            for movie in movies
            if self._rating(movie)
            >= min_rating
        ]

        filtered.sort(
            key=self._rating,
            reverse=True,
        )

        return filtered[:5]