from aiogram import BaseMiddleware
from typing import Callable, Any, Awaitable

from aiogram.types import TelegramObject

from app.models.config.main import BotConfig


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: BotConfig):
        self.config = config

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        data["forum_chat_id"] = self.config.forum_chat_id
        return await handler(event, data)
