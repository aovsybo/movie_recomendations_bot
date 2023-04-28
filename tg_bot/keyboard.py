from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton("/Случайный_фильм")
b2 = KeyboardButton("/Следующий")
b3 = KeyboardButton("/Похожий")
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.row(b1)
search_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
search_keyboard.row(b1)
search_keyboard.row(b2, b3)
