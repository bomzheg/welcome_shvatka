from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import UserDAO, ChatDAO
from app.dao.message import MessageDAO
from app.dao.topic import TopicDAO


@dataclass
class HolderDao:
    session: AsyncSession
    user: UserDAO = field(init=False)
    chat: ChatDAO = field(init=False)
    message: MessageDAO = field(init=False)
    topic: TopicDAO = field(init=False)

    def __post_init__(self):
        self.user = UserDAO(self.session)
        self.chat = ChatDAO(self.session)
        self.message = MessageDAO(self.session)
        self.topic = TopicDAO(self.session)

    async def commit(self):
        await self.session.commit()
