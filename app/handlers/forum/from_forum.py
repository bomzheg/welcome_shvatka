from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.dao.holder import HolderDao
from app.models.config.main import BotConfig


async def note(_message: Message):
    """
    Handler to messages which start with "!note" command.
    Such messages should be ignored.

    :param _message: any message which text or caption starts with "!note"
    """
    return


async def any_message(forum_message: Message, dao: HolderDao):
    topic = await dao.topic.get_by_topic(forum_message.message_thread_id)
    user = await dao.user.get_by_id(topic.user_id)
    user_message = await forum_message.send_copy(
        chat_id=user.tg_id,
    )
    await dao.message.save_message_pair(
        user=user,
        user_message_id=user_message.message_id,
        forum_message_id=forum_message.message_id,
        from_admin=True,
    )
    await dao.commit()


def setup(config: BotConfig) -> Router:
    router = Router(name=__name__)
    router.message.filter(F.chat.id == config.forum_chat_id)
    router.message.register(note, Command(commands="note", prefix="!/"))
    router.message.register(any_message)
    return router
