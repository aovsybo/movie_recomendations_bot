import requests

from config import settings
from model import is_movie_banned, ban_movie_for_user


# TODO: Сделать полнотекстовой запрос
# TODO: Сделать по режиссеру
# TODO: Сделать по стране
# TODO: Разобраться с конфигом
def get_movie(filters: dict, user_id: str):
    filters["selectFields"] = settings.SELECT_FIELDS
    filters["limit"] = settings.MOVIE_SEARCH_LIMIT
    filters["page"] = 1
    movie = None
    while True:
        request = requests.get(
            f"{settings.KP_API_ADDRESS}v1.3/movie",
            headers={"X-API-KEY": settings.KP_API_TOKEN},
            params=filters
        ).json()
        try:
            movies = request["docs"]
        except Exception:
            return {"error": 'Ошибка запроса'}
        else:
            if len(movies) > 0:
                for cur_movie in movies:
                    if not is_movie_banned(user_id, str(cur_movie["id"])):
                        movie = cur_movie
                        break
                if movie is not None:
                    ban_movie_for_user(user_id, movie["id"])
                    return movie
                else:
                    filters["page"] += 1
            else:
                return {"error": 'Не найдено фильмов'}


def get_random_movie():
    params = {
        "selectFields": settings.SELECT_FIELDS
    }
    movie = requests.get(
        f"{settings.KP_API_ADDRESS}v1.3/movie/random",
        headers={"X-API-KEY": settings.KP_API_TOKEN},
        params=params
    ).json()
    return movie


def get_country_names():
    filters = {"field": "countries.name"}
    countries = requests.get(
        f"{settings.KP_API_ADDRESS}v1/movie/possible-values-by-field",
        headers={"X-API-KEY": settings.KP_API_TOKEN},
        params=filters
    ).json()
    return [country["name"] for country in countries]
