from sqlalchemy import ScalarResult, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import BaseDAO
from app.models import db, dto


class MessageDAO(BaseDAO[db.Message]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.Message, session)

    async def save_message_pair(
        self,
        user: dto.User,
        user_message_id: int,
        forum_message_id: int,
        from_admin: bool,
    ) -> dto.Message:
        message = db.Message(
            user_id=user.db_id,
            user_message_id=user_message_id,
            forum_message_id=forum_message_id,
            from_admin=from_admin,
        )
        self._save(message)
        await self.flush(message)
        return message.to_dto()

    async def get_by_forum_message_id(self, forum_message_id: int) -> dto.Message | None:
        result: ScalarResult[db.Message] = await self.session.scalars(
            select(db.Message)
            .where(db.Message.forum_message_id == forum_message_id)
        )
        try:
            return result.one().to_dto()
        except NoResultFound:
            return None

    async def get_by_user_message_id(self, user_message_id: int) -> dto.Message | None:
        result: ScalarResult[db.Message] = await self.session.scalars(
            select(db.Message)
            .where(db.Message.user_message_id == user_message_id)
        )
        try:
            return result.one().to_dto()
        except NoResultFound:
            return None

