from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.types import Message

from app.dao.holder import HolderDao
from app.models import dto
from app.services.messages import any_message


async def any_message_handler(user_message: Message, user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int):
    return await any_message(user_message, user, dao, bot, forum_chat_id)


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.message.register(any_message_handler)
    return router
