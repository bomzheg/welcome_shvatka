from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

WANT_RETURN = "Я уже играл в Схватку раньше, хочу вернуться"
WANT_KNOW = "Хочу узнать больше о Схватке"
WANT_PLAY = "Хочу сыграть в Схватку"


def get_start_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=WANT_PLAY)
    builder.button(text=WANT_KNOW)
    builder.button(text=WANT_RETURN)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
