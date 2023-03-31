from aiogram.utils import executor

from tg_bot.create_bot import dp
from tg_bot.view import register_handlers


async def on_startup(_):
    print("Бот онлайн")


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
