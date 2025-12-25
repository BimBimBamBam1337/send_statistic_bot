from typing import Any, Awaitable, Callable, Dict
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from loguru import logger
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.database.engine import SessionFactory
from src.presentation.google import GoogleSheetsAsync


class DependanciesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["uow"] = UnitOfWork(SessionFactory)
        data["google_sheet"] = GoogleSheetsAsync()
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"An error ocured: {e}")


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler):
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        data["scheduler"] = self.scheduler
        return await handler(event, data)
