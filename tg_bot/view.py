from aiogram import types, Dispatcher

from config import settings
from services.kinopoisk import get_movie, get_random_movie
from services.text_analysis import text_analyse
from tg_bot.create_bot import bot
from tg_bot.keyboard import search_keyboard, start_keyboard


async def configure_message_by_filters(filters: dict):
    if "error" in filters.keys():
        return filters["error"]
    else:
        return f"Советую посмотреть {settings.TYPE_NAME_BY_TYPE_NUMBER[filters['typeNumber']]} \"{filters['name']}\" " \
           f"{filters['year']} года с оценкой {round(filters['rating']['kp'], 1)}\n"


async def send_movie(movie: dict, user_id: str, keyboard):
    if "poster" in movie.keys():
        await bot.send_photo(
            user_id,
            movie['poster']['url'],
            await configure_message_by_filters(movie),
            reply_markup=keyboard,
        )
    else:
        await bot.send_message(
            user_id,
            await configure_message_by_filters(movie),
            reply_markup=keyboard,
        )


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Могу помочь с выбором фильма!", reply_markup=start_keyboard)


# @dp.message_handler(commands=["/Случайный_фильм"])
async def recommend_random_movie(message: types.Message):
    movie = get_random_movie()
    await send_movie(movie, message.from_user.id, start_keyboard)


# @dp.message_handler(commands=["/Следующий"])
async def recommend_other_movie_by_filters(message: types.Message):
    movie_filters = getattr(settings, "PREV_MOVIE_FILTERS")
    movie = get_movie(movie_filters, str(message.from_user.id))
    await send_movie(movie, message.from_user.id, search_keyboard)


# @dp.message_handler(commands=[])
async def recommend_movie_by_filters(message: types.Message):
    movie_filters = text_analyse(message.text)
    setattr(settings, "PREV_MOVIE_FILTERS", movie_filters)
    movie = get_movie(movie_filters, str(message.from_user.id))
    await send_movie(movie, message.from_user.id, search_keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(recommend_random_movie, commands=["Случайный_фильм"])
    dp.register_callback_query_handler(recommend_other_movie_by_filters, text="Следующий")
    dp.register_message_handler(recommend_movie_by_filters)
