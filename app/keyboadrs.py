from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Хочу попробовать сыграть в Схватку")
    builder.button(text="Хочу узнать больше о Схватке")
    builder.button(text="Я уже играл в Схватку раньше, хочу вернуться")
    return builder.as_markup(resize_keyboard=True)
