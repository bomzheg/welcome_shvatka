import enum

from aiogram import Bot, Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from app.keyboadrs import WANT_PLAY, WANT_KNOW, WANT_RETURN
from app.models import dto
from app.views.user import user_link


class GameInfoRequestType(enum.Enum):
    try_game = enum.auto()
    about_game = enum.auto()


async def try_game_handler(m: Message, user: dto.User, bot: Bot, admin_id: int):
    await notify_admin(admin_id, user, GameInfoRequestType.try_game, bot)
    await m.reply(
        "Привет! Рады видеть тебя в нашем сообществе. "
        "Скоро с тобой свяжется один из капитанов и обязательно возьмет в команду.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def about_game_handler(m: Message, user: dto.User, bot: Bot, admin_id: int):
    await notify_admin(admin_id, user, GameInfoRequestType.about_game, bot)
    await m.reply(
        "Привет! Рады, что ты заинтересовался игрой. "
        "Скоро с тобой свяжется один из капитанов и ответит на все вопросы.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def returning_to_game_handler(m: Message):
    await m.reply(
        "Привет! Рады твоему возвращению. "
        "Ты уже знаешь, что игроки в схватку - самые дружелюбные люди в Лыткарино. "
        "Присоединяйся к нашему telegram-каналу (@shvatka_lytkarino). "
        "Там ты наверняка найдешь старых знакомых или новую команду. "
        "Или напиши капитану @pblgblk",
        reply_markup=ReplyKeyboardRemove(),
    )


async def notify_admin(admin_id: int, user: dto.User, request_type: GameInfoRequestType, bot: Bot):
    match request_type:
        case GameInfoRequestType.try_game:
            await bot.send_message(chat_id=admin_id, text=f"{user_link(user)} хочет попробовать сыграть в Схватку")
        case GameInfoRequestType.about_game:
            await bot.send_message(chat_id=admin_id, text=f"{user_link(user)} хочет узнать больше о Схватке")


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(try_game_handler, F.text == WANT_PLAY)
    router.message.register(about_game_handler, F.text == WANT_KNOW)
    router.message.register(returning_to_game_handler, F.text == WANT_RETURN)
    return router
