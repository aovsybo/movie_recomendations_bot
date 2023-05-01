import os
from datetime import date

from pydantic import BaseSettings, HttpUrl
from dotenv import find_dotenv, load_dotenv


class Settings(BaseSettings):
    KP_API_ADDRESS: HttpUrl = "https://api.kinopoisk.dev/v1.3"
    TG_API_TOKEN: str
    KP_API_TOKEN: str
    CURRENT_YEAR = int(date.today().strftime("%Y"))
    START_SEARCH_FROM_YEAR = CURRENT_YEAR - 15
    MIN_YEAR = 1900
    MAX_KP_RATING = 10.0
    START_KP_RATING = 7.0
    MIN_KP_RATING = 1.0
    MOVIE_SEARCH_LIMIT = 10
    SELECT_FIELDS = ["id", "name", "rating.kp", "year",  "poster.url", 'typeNumber']
    TYPE_NUMBER_BY_TYPE_NAME = {
        "фильм": 1,
        "сериал": 2,
        "мультик": 3, "мультфильм": 3,
        "аниме": 4,
        "мультсериал": 5, "мультисериал": 5,
        "шоу": 6, "тв-шоу": 6, "твшоу": 6,
    }
    TYPE_NAME_BY_TYPE_NUMBER = {
        1: "фильм",
        2: "сериал",
        3: "мультфильм",
        4: "аниме",
        5: "мультсериал",
        6: "тв-шоу",
    }
    USER_DATA_DIR_NAME = "userdata"
    PREV_MOVIE_FILTERS = dict()
    GENRE_NAMES = ['аниме', 'биография', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'документальный',
                   'драма', 'история', 'комедия', 'криминал', 'мелодрама', 'музыка', 'мультфильм', 'мюзикл',
                   'приключения', 'семейный', 'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фэнтези']
    RATING_WORDS = ["оценка", "балл", "рейтинг"]
    YEAR_FROM_WORDS = ["от", "после", "младше", "с"]
    YEAR_UNTIL_WORDS = ["до", "старше"]
    RATING_FROM_WORDS = ["от", "выше", "больше"]
    RATING_UNTIL_WORDS = ["до", "ниже", "меньше"]

    def __init__(self):
        load_dotenv(find_dotenv())
        TG_API_TOKEN = os.environ.get("TG_API_TOKEN")
        KP_API_TOKEN = os.environ.get("KP_API_TOKEN")
        super().__init__()


settings = Settings()
