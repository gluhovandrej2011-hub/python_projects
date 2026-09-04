from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    """Класс для работы с подключением к PostgreSQL."""

    def __init__(self, database_url: str):
        self.engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=False,
        )

        self.session_factory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    def create_tables(self, base):
        """Создаёт таблицы."""

        base.metadata.create_all(
            self.engine
        )

    def get_session(self):
        """Создаёт новую сессию."""

        return self.session_factory()