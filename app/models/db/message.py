# from https://github.com/MasterGroosha/telegram-feedback-bot-topics
from sqlalchemy import UniqueConstraint, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .. import dto


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        UniqueConstraint(
            'user_id', 'user_message_id', 'forum_message_id',
            name='unique_messages_ids_combinations'
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="messages", foreign_keys=user_id, uselist=False)
    user_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    forum_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    from_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_dto(self) -> dto.Message:
        return dto.Message(
            id=self.id,
            user_id=self.user_id,
            user_message_id=self.user_message_id,
            forum_message_id=self.forum_message_id,
            from_admin=self.from_admin,
        )
