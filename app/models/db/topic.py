# from https://github.com/MasterGroosha/telegram-feedback-bot-topics
from sqlalchemy import UniqueConstraint, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import dto
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
    user = relationship("User", back_populates="topic", foreign_keys=user_id, uselist=False)
    topic_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_message_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dto(self) -> dto.Topic:
        return dto.Topic(
            id=self.id,
            user_id=self.user_id,
            topic_id=self.topic_id,
            start_message_id=self.start_message_id,
        )
