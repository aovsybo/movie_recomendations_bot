import os

from config import settings


def ban_movie_for_user(user_id: str, movie_id: str):
    if not os.path.exists(settings.USER_DATA_DIR_NAME):
        os.mkdir(settings.USER_DATA_DIR_NAME)
    with open(f'userdata/{user_id}', 'a') as banned_movies:
        banned_movies.write(f"{str(movie_id)}, ")


def is_movie_banned(user_id: str, movie_id: str) -> bool:
    try:
        with open(f'userdata/{user_id}', 'r') as banned_movies:
            set_of_banned_movies = set(banned_movies.read().split(', '))
            return movie_id in set_of_banned_movies
    except IOError:
        return False
