from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/Случайный_фильм")
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.row(b1)
