from collections import namedtuple
import requests

from config import settings


def configure_movie_string(movie):
    return f"\"{movie['name']}\" {movie['year']} года с оценкой {round(movie['rating']['kp'], 1)}\n"


def get_movie(filters: dict):
    headers = {
        "X-API-KEY": settings.KP_API_TOKEN,
    }
    # params = {
    #     "genre.name": filters["genre"],
    #     "year": filters["year"],
    #     "rating.kp": filters["rating"],
    #     "selectFields": ["name", "rating.kp", "year"],
    #     "limit": 1,
    # }
    filters["selectFields"] = ["name", "rating.kp", "year"]
    filters["limit"] = 1

    print(filters)
    movies = requests.get(f"{settings.KP_API_ADDRESS}/movie", headers=headers, params=filters).json()["docs"]
    amount_of_movies = len(movies)
    if amount_of_movies == 0:
        response = "Не найдено фильмов"
    elif amount_of_movies == 1:
        movie = movies[0]
        response = "Советую посмотреть фильм" + configure_movie_string(movie)
    elif amount_of_movies > 1:
        response = f"Найдено фильмов: {amount_of_movies}. Советую посмотреть:\n"
        for movie in movies:
            response += configure_movie_string(movie)
    else:
        response = "Ошибка"
    return response


def get_random_movie():
    headers = {
        "X-API-KEY": settings.KP_API_TOKEN
    }
    params = {
        "selectFields": ["name", "year"]
    }
    response = requests.get(f"{settings.KP_API_ADDRESS}/movie/random", headers=headers, params=params).json()
    movie = {
        "name": response["name"],
        "rating": response["rating"]["imdb"],
        "year": response["year"],
    }
    return f"Советую посмотреть фильм \"{movie['name']}\" {movie['year']} года с оценкой {movie['rating']}"
