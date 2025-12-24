from typing import Any, Awaitable, Callable, Dict
from datetime import datetime, timedelta

from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from loguru import logger
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.database.engine import SessionFactory


class DependanciesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["uow"] = UnitOfWork(SessionFactory)
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"An error ocured: {e}")
