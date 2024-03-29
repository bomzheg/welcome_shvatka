import logging

from aiogram import Dispatcher

from app.handlers import welcome, forum
from app.handlers.base import setup_base
from app.handlers.errors import setup_errors
from app.handlers.superuser import setup_superuser
from app.models.config.main import BotConfig

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    setup_errors(dp, bot_config.log_chat)
    setup_base(dp)
    dp.include_router(welcome.setup())
    dp.include_router(forum.setup(bot_config))
    setup_superuser(dp, bot_config)
    logger.debug("handlers configured successfully")
