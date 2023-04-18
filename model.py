import json


def ban_movie_for_user(user_id: str, movie_id: int):
    with open('userdata.json', 'r') as file_read:
        config = dict(json.loads(file_read.read()))
    if user_id not in config:
        config[user_id] = [movie_id]
    else:
        config[user_id].append(movie_id)
    with open('userdata.json', 'w') as file_write:
        json.dump(config, file_write, indent=2)


def get_users_banned_movies(user_id: str) -> list[int]:
    with open('userdata.json', 'r') as file_read:
        config = dict(json.loads(file_read.read()))
    return config[user_id] if user_id in config else []

