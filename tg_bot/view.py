from aiogram import types, Dispatcher

from config import settings
from services.kinopoisk import get_movie, get_random_movie
from services.text_analysis import text_analyse
from tg_bot.create_bot import bot
from tg_bot.keyboard import search_keyboard, start_keyboard


# @dp.message_handler(commands=["start", "help"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Могу помочь с выбором фильма!", reply_markup=start_keyboard)


# @dp.message_handler(commands=["/Случайный_фильм"])
async def recommend_random_movie(message: types.Message):
    await bot.send_message(message.from_user.id, get_random_movie(), reply_markup=start_keyboard)


# @dp.message_handler(commands=["/Другой"])
async def recommend_other_movie_by_filters(message: types.Message):
    movie_filters = getattr(settings, "PREV_MOVIE_FILTERS")
    await bot.send_message(
        message.from_user.id,
        get_movie(movie_filters, str(message.from_user.id)),
        reply_markup=search_keyboard,
    )


# @dp.message_handler(commands=[])
async def recommend_movie_by_filters(message: types.Message):
    movie_filters = text_analyse(message.text)
    setattr(settings, "PREV_MOVIE_FILTERS", movie_filters)
    await bot.send_message(
        message.from_user.id,
        get_movie(movie_filters, str(message.from_user.id)),
        reply_markup=search_keyboard,
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(recommend_random_movie, commands=["Случайный_фильм"])
    dp.register_message_handler(recommend_other_movie_by_filters, commands=["Другой"])
    dp.register_message_handler(recommend_movie_by_filters)
