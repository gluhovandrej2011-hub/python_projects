import logging
from datetime import datetime

import telebot
from telebot import types

from servic import NinjasAPIError


class FilmWatcherBot:
    """Telegram-бот FilmWatcher."""

    def __init__(
        self,
        token: str,
        film_service,
    ):

        self.bot = telebot.TeleBot(
            token,
            parse_mode="HTML",
        )

        self.film_service = film_service

        # Состояния пользователей.
        self.states: dict[int, str] = {}

        # Временные данные пользователя.
        self.user_data: dict[int, dict] = {}

        self._register_handlers()

    # =====================================================
    # КЛАВИАТУРЫ
    # =====================================================

    @staticmethod
    def main_keyboard():

        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
        )

        keyboard.row(
            " Популярные фильмы",
        )

        keyboard.row(
            " Поиск фильма по жанру",
        )

        keyboard.row(
            " Просмотренные ранее",
        )

        return keyboard

    @staticmethod
    def cancel_keyboard():

        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
        )

        keyboard.row(" Отмена")

        return keyboard

    # =====================================================
    # УТИЛИТЫ
    # =====================================================

    @staticmethod
    def movie_title(movie: dict) -> str:

        return (
            movie.get("title")
            or movie.get("name")
            or "Без названия"
        )

    @staticmethod
    def movie_rating(movie: dict) -> float:

        value = (
            movie.get("rating")
            or movie.get("imdb_rating")
            or movie.get("imdbRating")
            or 0
        )

        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def movie_description(
        movie: dict,
    ) -> str:

        return (
            movie.get("description")
            or movie.get("plot")
            or movie.get("overview")
            or "Описание отсутствует."
        )

    def _register_handlers(self):

        @self.bot.message_handler(
            commands=["start"]
        )
        def start_handler(message):

            user_id = message.from_user.id

            self.states.pop(
                user_id,
                None,
            )

            self.user_data.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "<b>Добро пожаловать в FilmWatcher!</b>\n\n"
                "Я помогу тебе выбрать фильм "
                "для вечернего просмотра.\n\n"
                "Выбери действие:",
                reply_markup=self.main_keyboard(),
            )

        @self.bot.message_handler(
            commands=["help"]
        )
        def help_handler(message):

            self.bot.send_message(
                message.chat.id,
                " <b>FilmWatcher</b>\n\n"
                "Популярные фильмы — "
                "топ-3 фильма.\n\n"
                "Поиск — подборка по жанру "
                "и минимальному рейтингу.\n\n"
                "Просмотренные ранее — "
                "история выбранных фильмов.\n\n"
                "Для отмены ввода нажмите "
                "«Отмена».",
                reply_markup=self.main_keyboard(),
            )


        @self.bot.message_handler(
            func=lambda message:
            message.text == "Отмена"
        )
        def cancel_handler(message):

            user_id = message.from_user.id

            self.states.pop(
                user_id,
                None,
            )

            self.user_data.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "Действие отменено.",
                reply_markup=self.main_keyboard(),
            )

        @self.bot.message_handler(
            func=lambda message:
            message.text == "Популярные фильмы"
        )
        def popular_handler(message):

            try:

                movies = (
                    self.film_service
                    .get_popular_movies()
                )

                if not movies:

                    self.bot.send_message(
                        message.chat.id,
                        "Сейчас не удалось "
                        "найти фильмы.",
                    )

                    return

                self._send_movie_list(
                    message.chat.id,
                    movies,
                    "<b>3 самых популярных фильма:</b>",
                )

            except NinjasAPIError as error:

                logging.error(
                    "Ninjas API error: %s",
                    error,
                )

                self.bot.send_message(
                    message.chat.id,
                    "Не удалось получить "
                    "популярные фильмы.\n\n"
                    "Попробуйте позже.",
                )

            except Exception:

                logging.exception(
                    "Ошибка popular_handler"
                )

                self.bot.send_message(
                    message.chat.id,
                    "Произошла внутренняя ошибка.",
                )

        @self.bot.message_handler(
            func=lambda message:
            message.text == "Поиск фильма по жанру"
        )
        def search_start_handler(message):

            user_id = message.from_user.id

            self.states[user_id] = "waiting_genre"

            self.user_data[user_id] = {}

            self.bot.send_message(
                message.chat.id,
                "<b>Введите жанр фильма.</b>\n\n"
                "Например:\n"
                "Action\n"
                "Comedy\n"
                "Drama",
                reply_markup=self.cancel_keyboard(),
            )

        @self.bot.message_handler(
            func=lambda message:
            message.text == "Просмотренные ранее"
        )
        def history_handler(message):

            try:

                films = (
                    self.film_service
                    .get_history(
                        message.from_user.id
                    )
                )

                if not films:

                    self.bot.send_message(
                        message.chat.id,
                        "История пуста.\n\n"
                        "Сначала выберите фильм "
                        "из подборки.",
                        reply_markup=self.main_keyboard(),
                    )

                    return

                keyboard = (
                    types.InlineKeyboardMarkup()
                )

                for film in films:

                    keyboard.add(
                        types.InlineKeyboardButton(
                            text=film.movie_name,
                            callback_data=(
                                f"history:{film.id}"
                            ),
                        )
                    )

                text = (
                    "<b>Просмотренные ранее:</b>\n\n"
                    "Выберите фильм:"
                )

                self.bot.send_message(
                    message.chat.id,
                    text,
                    reply_markup=keyboard,
                )

            except Exception:

                logging.exception(
                    "Ошибка history_handler"
                )

                self.bot.send_message(
                    message.chat.id,
                    "Не удалось загрузить "
                    "историю.",
                )

        @self.bot.message_handler(
            func=lambda message:
            message.from_user.id in self.states
        )
        def state_handler(message):

            user_id = message.from_user.id

            state = self.states.get(
                user_id
            )

            if state == "waiting_genre":

                self._process_genre(
                    message
                )

            elif state == "waiting_rating":

                self._process_min_rating(
                    message
                )

            elif state == "waiting_review_rating":

                self._process_review_rating(
                    message
                )

            elif state == "waiting_note":

                self._process_note(
                    message
                )

        @self.bot.callback_query_handler(
            func=lambda call:
            call.data.startswith("movie:")
        )
        def select_movie_callback(call):

            try:

                index = int(
                    call.data.split(":")[1]
                )

                user_id = call.from_user.id

                data = self.user_data.get(
                    user_id
                )

                if not data:

                    self.bot.answer_callback_query(
                        call.id,
                        "Сессия поиска закончилась.",
                        show_alert=True,
                    )

                    return

                movies = data.get(
                    "movies",
                    []
                )

                if index < 0 or index >= len(movies):

                    self.bot.answer_callback_query(
                        call.id,
                        "Фильм не найден.",
                        show_alert=True,
                    )

                    return

                movie = movies[index]

                genre = data.get(
                    "genre",
                    "Не указан"
                )

                saved = (
                    self.film_service
                    .save_selected_movie(
                        tg_user_id=user_id,
                        movie=movie,
                        genre=genre,
                    )
                )

                title = self.movie_title(
                    movie
                )

                rating = self.movie_rating(
                    movie
                )

                description = (
                    self.movie_description(
                        movie
                    )
                )

                text = (
                    f"🎬 <b>{title}</b>\n\n"
                    f"🎭 Жанр: {genre}\n"
                    f"⭐ Рейтинг: {rating:.1f}\n\n"
                    f"📖 {description}\n\n"
                    "✅ Фильм сохранён в твоей "
                    "истории.\n\n"
                    "После просмотра можешь "
                    "поставить собственную оценку "
                    "и оставить заметку."
                )

                keyboard = (
                    types.InlineKeyboardMarkup()
                )

                keyboard.add(
                    types.InlineKeyboardButton(
                        text="⭐ Оценить фильм",
                        callback_data=(
                            f"review:{saved.id}"
                        ),
                    )
                )

                self.bot.send_message(
                    call.message.chat.id,
                    text,
                    reply_markup=keyboard,
                )

                self.bot.answer_callback_query(
                    call.id,
                    "Фильм сохранён!",
                )

                # Сохраняем ID выбранного фильма
                # в текущей сессии.
                self.user_data[user_id][
                    "selected_film_id"
                ] = saved.id

            except Exception:

                logging.exception(
                    "Ошибка select_movie_callback"
                )

                self.bot.answer_callback_query(
                    call.id,
                    "⚠️ Не удалось сохранить фильм.",
                    show_alert=True,
                )

        # -------------------------------------------------
        # CALLBACK: HISTORY
        # -------------------------------------------------

        @self.bot.callback_query_handler(
            func=lambda call:
            call.data.startswith("history:")
        )
        def history_callback(call):

            try:

                film_id = int(
                    call.data.split(":")[1]
                )

                film = (
                    self.film_service
                    .get_history_film(
                        call.from_user.id,
                        film_id,
                    )
                )

                if film is None:

                    self.bot.answer_callback_query(
                        call.id,
                        "Фильм не найден.",
                        show_alert=True,
                    )

                    return

                note = (
                    film.note
                    if film.note
                    else "Заметка отсутствует."
                )

                rating = (
                    str(film.rating_film)
                    if film.rating_film
                    else "Оценка не поставлена"
                )

                text = (
                    f"🎬 <b>{film.movie_name}</b>\n\n"
                    f"📅 Дата просмотра: "
                    f"{film.watched_at:%d.%m.%Y %H:%M}\n"
                    f"🎭 Жанр: {film.genre_name}\n"
                    f"⭐ Оценка: {rating}\n"
                    f"📝 Заметка: {note}"
                )

                keyboard = (
                    types.InlineKeyboardMarkup()
                )

                keyboard.add(
                    types.InlineKeyboardButton(
                        text="⭐ Изменить оценку",
                        callback_data=(
                            f"review:{film.id}"
                        ),
                    )
                )

                self.bot.send_message(
                    call.message.chat.id,
                    text,
                    reply_markup=keyboard,
                )

                self.bot.answer_callback_query(
                    call.id
                )

            except Exception:

                logging.exception(
                    "Ошибка history_callback"
                )

                self.bot.answer_callback_query(
                    call.id,
                    "⚠️ Произошла ошибка.",
                    show_alert=True,
                )

        # -------------------------------------------------
        # CALLBACK: REVIEW
        # -------------------------------------------------

        @self.bot.callback_query_handler(
            func=lambda call:
            call.data.startswith("review:")
        )
        def review_callback(call):

            try:

                film_id = int(
                    call.data.split(":")[1]
                )

                film = (
                    self.film_service
                    .get_history_film(
                        call.from_user.id,
                        film_id,
                    )
                )

                if film is None:

                    self.bot.answer_callback_query(
                        call.id,
                        "Фильм не найден.",
                        show_alert=True,
                    )

                    return

                user_id = call.from_user.id

                self.user_data.setdefault(
                    user_id,
                    {}
                )

                self.user_data[user_id][
                    "review_film_id"
                ] = film_id

                self.states[user_id] = (
                    "waiting_review_rating"
                )

                self.bot.send_message(
                    call.message.chat.id,
                    f"⭐ <b>{film.movie_name}</b>\n\n"
                    "Поставьте свою оценку "
                    "от 1 до 10:",
                    reply_markup=self.cancel_keyboard(),
                )

                self.bot.answer_callback_query(
                    call.id
                )

            except Exception:

                logging.exception(
                    "Ошибка review_callback"
                )

                self.bot.answer_callback_query(
                    call.id,
                    "⚠️ Не удалось открыть "
                    "форму оценки.",
                    show_alert=True,
                )

    # =====================================================
    # GENRE
    # =====================================================

    def _process_genre(
        self,
        message,
    ):

        user_id = message.from_user.id

        genre = (
            message.text or ""
        ).strip()

        if not genre:

            self.bot.send_message(
                message.chat.id,
                "❌ Жанр не может быть пустым.",
            )

            return

        if len(genre) > 50:

            self.bot.send_message(
                message.chat.id,
                "❌ Название жанра должно "
                "содержать не более 50 символов.",
            )

            return

        self.user_data[user_id][
            "genre"
        ] = genre

        self.states[user_id] = (
            "waiting_rating"
        )

        self.bot.send_message(
            message.chat.id,
            f"🎭 Жанр: <b>{genre}</b>\n\n"
            "⭐ Теперь введите минимальный "
            "рейтинг фильма от 0 до 10.\n\n"
            "Например: <code>7.5</code>",
        )

    # =====================================================
    # MIN RATING
    # =====================================================

    def _process_min_rating(
        self,
        message,
    ):

        user_id = message.from_user.id

        try:

            value = float(
                (message.text or "")
                .replace(",", ".")
            )

            if not 0 <= value <= 10:
                raise ValueError

        except ValueError:

            self.bot.send_message(
                message.chat.id,
                "❌ Введите число от 0 до 10.\n"
                "Например: <code>7.5</code>",
            )

            return

        genre = self.user_data[
            user_id
        ]["genre"]

        try:

            movies = (
                self.film_service
                .search_movies(
                    genre,
                    value,
                )
            )

            self.states.pop(
                user_id,
                None,
            )

            if not movies:

                self.bot.send_message(
                    message.chat.id,
                    "😔 Подходящих фильмов "
                    "не найдено.\n\n"
                    "Попробуйте другой жанр "
                    "или уменьшите рейтинг.",
                    reply_markup=self.main_keyboard(),
                )

                return

            self.user_data[user_id][
                "movies"
            ] = movies

            self._send_movie_list(
                message.chat.id,
                movies,
                (
                    "🎯 <b>Подходящие фильмы:</b>\n\n"
                    f"Жанр: {genre}\n"
                    f"Минимальный рейтинг: {value}\n\n"
                    "Выберите фильм:"
                ),
            )

        except NinjasAPIError:

            self.states.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "⚠️ Не удалось выполнить поиск.\n\n"
                "Попробуйте позже.",
                reply_markup=self.main_keyboard(),
            )

        except Exception:

            logging.exception(
                "Ошибка _process_min_rating"
            )

            self.states.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "⚠️ Произошла ошибка "
                "при поиске фильмов.",
                reply_markup=self.main_keyboard(),
            )

    # =====================================================
    # REVIEW RATING
    # =====================================================

    def _process_review_rating(
        self,
        message,
    ):

        user_id = message.from_user.id

        try:

            rating = int(
                (message.text or "").strip()
            )

            if not 1 <= rating <= 10:
                raise ValueError

        except ValueError:

            self.bot.send_message(
                message.chat.id,
                "❌ Оценка должна быть "
                "целым числом от 1 до 10.",
            )

            return

        film_id = self.user_data[
            user_id
        ].get("review_film_id")

        if not film_id:

            self.states.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "⚠️ Фильм для оценки не найден.",
                reply_markup=self.main_keyboard(),
            )

            return

        self.user_data[user_id][
            "review_rating"
        ] = rating

        self.states[user_id] = (
            "waiting_note"
        )

        self.bot.send_message(
            message.chat.id,
            "📝 Теперь напишите заметку "
            "о фильме.\n\n"
            "Можно написать <b>нет</b>, "
            "если заметка не нужна.\n\n"
            "Максимум — 1000 символов.",
        )

    # =====================================================
    # NOTE
    # =====================================================

    def _process_note(
        self,
        message,
    ):

        user_id = message.from_user.id

        note = (
            message.text or ""
        ).strip()

        if note.lower() == "нет":
            note = None

        elif len(note) > 1000:

            self.bot.send_message(
                message.chat.id,
                "❌ Заметка слишком длинная.\n"
                "Максимальная длина — 1000 символов.",
            )

            return

        data = self.user_data.get(
            user_id,
            {}
        )

        film_id = data.get(
            "review_film_id"
        )

        rating = data.get(
            "review_rating"
        )

        if not film_id or rating is None:

            self.states.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "⚠️ Данные оценки потеряны.",
                reply_markup=self.main_keyboard(),
            )

            return

        try:

            success = (
                self.film_service
                .add_review(
                    tg_user_id=user_id,
                    film_id=film_id,
                    rating=rating,
                    note=note,
                )
            )

            self.states.pop(
                user_id,
                None,
            )

            if success:

                self.bot.send_message(
                    message.chat.id,
                    "✅ <b>Оценка сохранена!</b>\n\n"
                    f"⭐ Твоя оценка: {rating}/10\n"
                    f"📝 Заметка: "
                    f"{note or 'без заметки'}",
                    reply_markup=self.main_keyboard(),
                )

            else:

                self.bot.send_message(
                    message.chat.id,
                    "⚠️ Не удалось найти "
                    "этот фильм.",
                    reply_markup=self.main_keyboard(),
                )

        except Exception:

            logging.exception(
                "Ошибка сохранения отзыва"
            )

            self.states.pop(
                user_id,
                None,
            )

            self.bot.send_message(
                message.chat.id,
                "⚠️ Не удалось сохранить "
                "оценку.",
                reply_markup=self.main_keyboard(),
            )

    # =====================================================
    # СПИСОК ФИЛЬМОВ
    # =====================================================

    def _send_movie_list(
        self,
        chat_id: int,
        movies: list[dict],
        heading: str,
    ):

        keyboard = (
            types.InlineKeyboardMarkup()
        )

        for index, movie in enumerate(
            movies
        ):

            title = self.movie_title(
                movie
            )

            rating = self.movie_rating(
                movie
            )

            keyboard.add(
                types.InlineKeyboardButton(
                    text=(
                        f"{index + 1}. "
                        f"{title} ⭐{rating:.1f}"
                    ),
                    callback_data=(
                        f"movie:{index}"
                    ),
                )
            )

        self.bot.send_message(
            chat_id,
            heading,
            reply_markup=keyboard,
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        logging.info(
            "FilmWatcher Telegram bot started"
        )

        # Если Telegram/API временно отвалился,
        # бот не завершается навсегда.
        while True:

            try:

                self.bot.infinity_polling(
                    timeout=30,
                    long_polling_timeout=30,
                )

            except Exception:

                logging.exception(
                    "Ошибка Telegram polling. "
                    "Перезапуск через 5 секунд."
                )

                import time

                time.sleep(5)