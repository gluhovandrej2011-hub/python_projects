import os

class Config:
    """Конфигурация приложения."""

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    NINJAS_API_KEY = os.getenv("NINJAS_API_KEY")

    NINJAS_MOVIES_URL = os.getenv(
        "NINJAS_MOVIES_URL",
        "https://api.api-ninjas.com/v1/movies"
    )

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "filmwatcher")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    @classmethod
    def database_url(cls) -> str:
        """Возвращает URL подключения SQLAlchemy."""

        return (
            "postgresql+psycopg://"
            f"{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}"
            f"/{cls.DB_NAME}"
        )

    @classmethod
    def validate(cls):
        """Проверяет наличие обязательных настроек."""

        required = {
            "BOT_TOKEN": cls.BOT_TOKEN,
            "NINJAS_API_KEY": cls.NINJAS_API_KEY,
            "DB_PASSWORD": cls.DB_PASSWORD,
        }

        missing = [
            name
            for name, value in required.items()
            if not value
        ]

        if missing:
            raise ValueError(
                "Не заданы переменные окружения: "
                + ", ".join(missing)
            )