from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import Router, Bot, F

from src.presentation.telegram.filters import AdminFilter
from src.infrastructure.database.uow import UnitOfWork

router = Router()


@router.message(Command("add_excel_tabel"), AdminFilter())
async def add_excel_tabel(message: Message, uow: UnitOfWork):
    pass
