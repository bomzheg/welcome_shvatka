from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message

from app.dao.holder import HolderDao
from app.models.config.main import BotConfig
from app.services.messages import found_reply_from_topic


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
    target_reply_message_id = None
    if reply_message_id := found_reply_from_topic(topic, forum_message):
        if message_pair := await dao.message.get_by_forum_message_id(reply_message_id):
            target_reply_message_id = message_pair.user_message_id
    user_message = await forum_message.send_copy(
        chat_id=user.tg_id,
        reply_to_message_id=target_reply_message_id,
        allow_sending_without_reply=True,
    )
    await dao.message.save_message_pair(
        user=user,
        user_message_id=user_message.message_id,
        forum_message_id=forum_message.message_id,
        from_admin=True,
    )
    await dao.commit()


async def edited_message(forum_message: Message, bot: Bot, dao: HolderDao):
    topic = await dao.topic.get_by_topic(forum_message.message_thread_id)
    user = await dao.user.get_by_id(topic.user_id)
    message_pair = await dao.message.get_by_forum_message_id(
        forum_message.message_id,
    )
    if forum_message.text:
        await bot.edit_message_text(
            chat_id=user.tg_id,
            message_id=message_pair.user_message_id,
            text=forum_message.text,
        )


def setup(config: BotConfig) -> Router:
    router = Router(name=__name__)
    router.message.filter(
        F.chat.id == config.forum_chat_id,
        F.message_thread_id,
        F.content_type.in_([
            ContentType.DICE,
            ContentType.ANIMATION,
            ContentType.AUDIO,
            ContentType.CONTACT,
            ContentType.DOCUMENT,
            ContentType.LOCATION,
            ContentType.PHOTO,
            ContentType.POLL,
            ContentType.STICKER,
            ContentType.TEXT,
            ContentType.VENUE,
            ContentType.VIDEO,
            ContentType.VIDEO_NOTE,
            ContentType.VOICE,
        ]),
    )
    router.message.register(note, Command(commands="note", prefix="!/"))
    router.message.register(any_message)
    router.edited_message.filter(
        F.chat.id == config.forum_chat_id,
        F.message_thread_id,
    )
    router.edited_message.register(edited_message)
    return router
