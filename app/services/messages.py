from aiogram import Bot
from aiogram.types import Message

from app.dao.holder import HolderDao
from app.exceptions import NoTopicFoundException
from app.models import dto
from app.views.user import user_link


async def any_message(user_message: Message, user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int) -> dto.Topic:
    topic = await create_topic(user, dao, bot, forum_chat_id)
    target_reply_message_id = None
    if reply_message_id := found_reply_from_user(user_message):
        if message_pair := await dao.message.get_by_user_message_id(reply_message_id):
            target_reply_message_id = message_pair.forum_message_id
    forum_message = await user_message.send_copy(
        chat_id=forum_chat_id,
        message_thread_id=topic.topic_id,
        reply_to_message_id=target_reply_message_id,
        allow_sending_without_reply=True
    )
    await dao.message.save_message_pair(
        user=user,
        user_message_id=user_message.message_id,
        forum_message_id=forum_message.message_id,
        from_admin=False,
    )
    await dao.commit()
    return topic


def found_reply_from_user(message: Message) -> int | None:
    if reply_message := message.reply_to_message:
        return reply_message.message_id
    return None


def found_reply_from_topic(topic: dto.Topic, message: Message) -> int | None:
    if reply_message := message.reply_to_message:
        if reply_message.message_id != topic.start_message_id:
            return reply_message.message_id
    return None


async def create_topic(user: dto.User, dao: HolderDao, bot: Bot, forum_chat_id: int) -> dto.Topic:
    try:
        topic = await dao.topic.get_by_user(user)
    except NoTopicFoundException:
        new_topic = await bot.create_forum_topic(forum_chat_id, user.name_mention[:127])
        first_message = await bot.send_message(
            chat_id=forum_chat_id,
            message_thread_id=new_topic.message_thread_id,
            text=f"{user_link(user)} начал общение с ботом",
        )
        topic = await dao.topic.create(
            user=user,
            topic_id=new_topic.message_thread_id,
            start_message_id=first_message.message_id,
        )
        await dao.commit()
    return topic
