import os

from pydantic import BaseSettings, HttpUrl
from dotenv import find_dotenv, load_dotenv


class Settings(BaseSettings):
    KP_API_ADDRESS: HttpUrl = "https://api.kinopoisk.dev/v1"
    TG_API_TOKEN: str
    KP_API_TOKEN: str

    def __init__(self):
        load_dotenv(find_dotenv())
        TG_API_TOKEN = os.environ.get("TG_API_TOKEN")
        KP_API_TOKEN = os.environ.get("KP_API_TOKEN")
        super().__init__()


settings = Settings()
