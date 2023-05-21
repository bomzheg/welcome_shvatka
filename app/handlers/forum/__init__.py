from aiogram import Router

from app.handlers.forum import from_forum, from_users
from app.models.config.main import BotConfig


def setup(config: BotConfig) -> Router:
    router = Router()
    router.include_router(from_forum.setup(config))
    router.include_router(from_users.setup())
    return router
