from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from config import settings

bot = Bot(token=settings.TG_API_TOKEN)
dp = Dispatcher(bot)
