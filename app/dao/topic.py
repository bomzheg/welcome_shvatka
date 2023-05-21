from sqlalchemy import select, ScalarResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app import exceptions
from app.dao import BaseDAO
from app.models import db, dto


class TopicDAO(BaseDAO[db.Topic]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.Topic, session)

    async def get_by_user(self, user: dto.User) -> dto.Topic:
        result: ScalarResult[db.Topic] = await self.session.scalars(
            select(db.Topic)
            .where(db.Topic.user_id == user.db_id)
        )
        try:
            return result.one().to_dto()
        except NoResultFound as e:
            raise exceptions.NoTopicFoundException from e

    async def get_by_topic(self, topic_id: int) -> dto.Topic:
        result: ScalarResult[db.Topic] = await self.session.scalars(
            select(db.Topic)
            .where(db.Topic.topic_id == topic_id)
        )
        return result.one().to_dto()

    async def create(self, user: dto.User, topic_id: int, start_message_id: int) -> dto.Topic:
        topic = db.Topic(
            user_id=user.db_id,
            topic_id=topic_id,
            start_message_id=start_message_id,
        )
        self._save(topic)
        await self.flush(topic)
        return topic.to_dto()


