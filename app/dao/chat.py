from sqlalchemy import ScalarResult
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao import BaseDAO
from app.models import dto, db


class ChatDAO(BaseDAO[db.Chat]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.Chat, session)

    async def _get_by_tg_id(self, tg_id: int) -> db.Chat:
        result: ScalarResult[db.Chat] = await self.session.scalars(
            select(db.Chat).where(db.Chat.tg_id == tg_id)
        )
        return result.one()

    async def upsert_chat(self, chat: dto.Chat) -> dto.Chat:
        kwargs = dict(tg_id=chat.tg_id, title=chat.title, username=chat.username, type=chat.type)
        saved_chat = await self.session.scalars(
            insert(db.Chat)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(db.Chat.tg_id,), set_=kwargs, where=db.Chat.tg_id == chat.tg_id
            )
            .returning(db.Chat)
        )
        return saved_chat.one().to_dto()

    async def update_chat_id(self, chat: dto.Chat, new_id: int):
        chat_db = await self._get_by_tg_id(chat.tg_id)
        chat_db.tg_id = new_id
        self._save(chat_db)
