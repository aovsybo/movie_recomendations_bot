import os
from datetime import date

from pydantic import BaseSettings, HttpUrl
from dotenv import find_dotenv, load_dotenv


class Settings(BaseSettings):
    KP_API_ADDRESS: HttpUrl = "https://api.kinopoisk.dev/v1.3"
    TG_API_TOKEN: str
    KP_API_TOKEN: str
    CURRENT_YEAR = date.today().strftime("%Y")
    MAX_KP_RATING = 10
    MOVIE_SEARCH_LIMIT = 10
    SELECT_FIELDS = ["id", "name", "rating.kp", "year",  "poster.url"]
    USER_DATA_DIR_NAME = "userdata"
    PREV_MOVIE_FILTERS = dict()
    GENRE_NAMES = ['аниме', 'биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'документальный',
                   'драма', 'история', 'комедия', 'криминал', 'мелодрама', 'музыка', 'мультфильм', 'мюзикл',
                   'приключения', 'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фэнтези']
    RATING_NAMES = ["оценка", "рейтинг"]
    YEAR_NAMES = ["год"]

    def __init__(self):
        load_dotenv(find_dotenv())
        TG_API_TOKEN = os.environ.get("TG_API_TOKEN")
        KP_API_TOKEN = os.environ.get("KP_API_TOKEN")
        super().__init__()


settings = Settings()
