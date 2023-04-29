from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton("/Случайный_фильм")
b2 = InlineKeyboardButton("Следующий", callback_data="Следующий")
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.row(b1)
search_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
search_keyboard.add(b2)
