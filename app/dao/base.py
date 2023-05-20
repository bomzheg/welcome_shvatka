from sqlalchemy import delete, func, ScalarResult
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Type, Generic, Sequence

from app.models.db.base import Base


Model = TypeVar('Model', Base, Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> Sequence[Model]:
        result: ScalarResult[Model] = await self.session.scalars(select(self.model))
        return result.all()

    async def get_by_id(self, id_: int) -> Model:
        result: ScalarResult[Model] = await self.session.scalars(
            select(self.model).where(self.model.id == id_)
        )
        return result.one()

    def save(self, obj: Model):
        self.session.add(obj)

    async def delete_all(self):
        await self.session.execute(
            delete(self.model)
        )

    async def count(self):
        result: ScalarResult[int] = await self.session.scalars(
            select(func.count(self.model.id))
        )
        return result.one()

    async def commit(self):
        await self.session.commit()

    async def flush(self, *objects):
        await self.session.flush(objects)
