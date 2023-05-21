from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models import dto, db


class UserDAO(BaseDAO[db.User]):
    def __init__(self, session: AsyncSession):
        super().__init__(db.User, session)

    async def get_by_tg_id(self, tg_id: int) -> db.User:
        result = await self.session.execute(
            select(db.User).where(db.User.tg_id == tg_id)
        )
        return result.scalar_one()

    async def get_by_id(self, id_: int) -> dto.User:
        return (await self._get_by_id(id_)).to_dto()

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = dict(
            tg_id=user.tg_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_bot=user.is_bot,
        )
        saved_user = await self.session.execute(
            insert(db.User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(db.User.tg_id,), set_=kwargs, where=db.User.tg_id == user.tg_id
            )
            .returning(db.User)
        )
        return saved_user.scalar_one().to_dto()
