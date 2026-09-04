import logging

from config import Config

from db import Database
from models import Base
from film_rep import FilmRepository

from film_serv import FilmService

from servic import NinjasAPI

from bot import FilmWatcherBot


def main():

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    try:

        Config.validate()

        database = Database(
            Config.database_url()
        )

        database.create_tables(
            Base
        )

        logging.info(
            "Database initialized"
        )

        repository = FilmRepository(
            database
        )

        ninjas_api = NinjasAPI(
            api_key=Config.NINJAS_API_KEY,
            base_url=Config.NINJAS_MOVIES_URL,
        )

        film_service = FilmService(
            repository=repository,
            ninjas_api=ninjas_api,
        )

        bot = FilmWatcherBot(
            token=Config.BOT_TOKEN,
            film_service=film_service,
        )

        bot.run()

    except Exception:

        logging.exception(
            "Ошибка запуска приложения"
        )


if __name__ == "__main__":
    main()