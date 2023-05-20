# from https://github.com/MasterGroosha/telegram-feedback-bot-topics
from sqlalchemy import UniqueConstraint, BigInteger, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        UniqueConstraint(
            'from_chat_id', 'from_message_id', 'to_chat_id', 'to_message_id',
            name='unique_messages_ids_combinations'
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    from_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    from_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    to_chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    to_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    incoming: Mapped[bool] = mapped_column(Boolean, nullable=False)
