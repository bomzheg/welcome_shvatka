import enum

from aiogram import Bot, Router, F
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.enums import ChatType
from aiogram.types import Message, ReplyKeyboardRemove

from app.dao.holder import HolderDao
from app.keyboadrs import WANT_PLAY, WANT_KNOW, WANT_RETURN
from app.models import dto
from app.services.messages import any_message
from app.views.user import user_link


class GameInfoRequestType(enum.Enum):
    try_game = enum.auto()
    about_game = enum.auto()
    returning = enum.auto()


async def try_game_handler(m: Message, user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int):
    await m.reply(
        "Привет! Рады видеть тебя в нашем сообществе. "
        "Скоро с тобой свяжется один из капитанов и обязательно возьмет в команду.",
        reply_markup=ReplyKeyboardRemove(),
    )
    topic = await any_message(m, user, dao, bot, forum_chat_id)
    await notify_admin(forum_chat_id, topic, user, GameInfoRequestType.try_game, bot)


async def about_game_handler(m: Message, user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int):
    await m.reply(
        "Привет! Рады, что ты заинтересовался игрой. "
        "Скоро с тобой свяжется один из капитанов и ответит на все вопросы.",
        reply_markup=ReplyKeyboardRemove(),
    )
    topic = await any_message(m, user, dao, bot, forum_chat_id)
    await notify_admin(forum_chat_id, topic, user, GameInfoRequestType.about_game, bot)


async def returning_to_game_handler(m: Message, user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int):
    await m.reply(
        "Привет! Рады твоему возвращению. "
        "Ты уже знаешь, что игроки в схватку - самые дружелюбные люди в Лыткарино. "
        "Присоединяйся к нашему telegram-каналу (@shvatka_lytkarino). "
        "Там ты наверняка найдешь старых знакомых или новую команду. "
        "Или напиши капитану @pblgblk",
        reply_markup=ReplyKeyboardRemove(),
    )
    topic = await any_message(m, user, dao, bot, forum_chat_id)
    await notify_admin(forum_chat_id, topic, user, GameInfoRequestType.try_game, bot)


async def notify_admin(
    forum_chat_id: int,
    topic: dto.Topic,
    user: dto.User,
    request_type: GameInfoRequestType,
    bot: Bot,
):
    text = f"{user_link(user)} "
    match request_type:
        case GameInfoRequestType.try_game:
            text += "хочет попробовать сыграть в Схватку"
        case GameInfoRequestType.about_game:
            text += "хочет узнать больше о Схватке"
        case GameInfoRequestType.returning:
            text += "хочет вернуться"
    await bot.send_message(
        chat_id=forum_chat_id,
        message_thread_id=topic.topic_id,
        text=text,
    )


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.message.register(try_game_handler, F.text == WANT_PLAY)
    router.message.register(about_game_handler, F.text == WANT_KNOW)
    router.message.register(returning_to_game_handler, F.text == WANT_RETURN)
    return router
