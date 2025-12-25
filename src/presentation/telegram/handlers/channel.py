from loguru import logger
from aiogram import Router, Bot, F
from aiogram.types import ChatMemberUpdated, Message
from aiogram.enums.chat_member_status import ChatMemberStatus

from src.presentation.google import GoogleSheetsAsync
from src.presentation.telegram import texts
from src.presentation.telegram.constans import ADMIN_ID
from src.infrastructure.database.uow import UnitOfWork

router = Router()


@router.my_chat_member(
    F.new_chat_member.status == ChatMemberStatus.MEMBER,
    F.new_chat_member.user.is_bot,
)
async def on_bot_added_to_channel(
    event: ChatMemberUpdated,
):
    bot = event.bot
    for admin in ADMIN_ID:
        await bot.send_message(
            chat_id=admin, text=texts.channel_added(event.chat.title, event.chat.id)
        )
        logger.info(f"Добавил группу {event.chat.title}: {event.chat.id}")


@router.my_chat_member(
    F.new_chat_member.status == ChatMemberStatus.LEFT,
    F.new_chat_member.user.is_bot,
)
async def on_bot_kicked_from_channel(event: ChatMemberUpdated):
    bot = event.bot
    for admin in ADMIN_ID:
        await bot.send_message(
            chat_id=admin, text=texts.channel_added(event.chat.title, event.chat.id)
        )
        logger.info(f"Убралл группу {event.chat.title}: {event.chat.id}")
