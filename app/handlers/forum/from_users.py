from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.types import Message

from app.dao.holder import HolderDao
from app.models import dto
from app.services.messages import any_message


async def any_message_handler(user_message: Message, user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int):
    return await any_message(user_message, user, dao, bot, forum_chat_id)


async def edited_message(user_message: Message, bot: Bot, dao: HolderDao, forum_chat_id: int):
    message_pair = await dao.message.get_by_user_message_id(
        user_message.message_id,
    )
    if user_message.text:
        await bot.edit_message_text(
            chat_id=forum_chat_id,
            message_id=message_pair.forum_message_id,
            text=user_message.text,
        )


def setup() -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.edited_message.filter(F.chat.type == ChatType.PRIVATE)
    router.message.register(any_message_handler)
    router.edited_message.register(edited_message)
    return router
