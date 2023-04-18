import requests

from config import settings
from model import get_users_banned_movies, ban_movie_for_user


def configure_movie_string(movie):
    return f"Советую посмотреть фильм \"{movie['name']}\" " \
           f"{movie['year']} года с оценкой {round(movie['rating']['kp'], 1)}\n"


def get_movie(filters: dict, user_id: str):
    headers = {
        "X-API-KEY": settings.KP_API_TOKEN,
    }
    filters["selectFields"] = ["id", "name", "rating.kp", "year"]
    filters["limit"] = settings.MOVIE_SEARCH_LIMIT
    offset = 0
    banned_ids = get_users_banned_movies(user_id)
    movie = None
    while True:
        request = requests.get(f"{settings.KP_API_ADDRESS}/movie", headers=headers, params=filters).json()
        try:
            movies = request["docs"]
        except Exception:
            return "Ошибка запроса"
        else:
            if len(movies) > 0:
                for cur_movie in movies[offset:]:
                    if cur_movie["id"] not in banned_ids:
                        movie = cur_movie
                        break
                if movie is not None:
                    ban_movie_for_user(user_id, movie["id"])
                    return configure_movie_string(movie)
                else:
                    offset += settings.MOVIE_SEARCH_LIMIT
                    filters["limit"] += settings.MOVIE_SEARCH_LIMIT
            else:
                return "Не найдено фильмов"


def get_random_movie():
    headers = {
        "X-API-KEY": settings.KP_API_TOKEN
    }
    params = {
        "selectFields": ["id", "name", "rating.kp", "year"]
    }
    movie = requests.get(f"{settings.KP_API_ADDRESS}/movie/random", headers=headers, params=params).json()
    return configure_movie_string(movie)

