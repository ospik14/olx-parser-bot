from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔍 Мої пошуки'), 
            KeyboardButton(text='➕ Додати')
        ],
        [
            KeyboardButton(text='ℹ️ Допомога'),
            KeyboardButton(text='⭐ Преміум')
        ]
    ],
    resize_keyboard=True
)