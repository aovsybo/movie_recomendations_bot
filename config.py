import os
from datetime import date

from pydantic import BaseSettings, HttpUrl
from dotenv import find_dotenv, load_dotenv


class Settings(BaseSettings):
    KP_API_ADDRESS: HttpUrl = "https://api.kinopoisk.dev/v1"
    TG_API_TOKEN: str
    KP_API_TOKEN: str
    CURRENT_YEAR = date.today().strftime("%Y")
    MAX_KP_RATING = 10
    MOVIE_SEARCH_LIMIT = 10
    PREV_MOVIE_FILTERS = dict()

    def __init__(self):
        load_dotenv(find_dotenv())
        TG_API_TOKEN = os.environ.get("TG_API_TOKEN")
        KP_API_TOKEN = os.environ.get("KP_API_TOKEN")
        super().__init__()

    def get_movie_filters(self):
        return getattr(self, "_prev_movie_filters")

    def set_movie_filters(self, movie_filters):
        setattr(self, "_prev_movie_filters", movie_filters)


settings = Settings()
