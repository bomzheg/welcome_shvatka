# from https://github.com/MasterGroosha/telegram-feedback-bot-topics
from sqlalchemy import UniqueConstraint, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db import Base


class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (
        UniqueConstraint(
            'user_id', 'topic_id',
            name='unique_topics_pairs'
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    topic_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_message_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def dict(self):
        return {
            "user_id": self.user_id,
            "topic_id": self.topic_id,
            "first_message_id": self.first_message_id
        }
