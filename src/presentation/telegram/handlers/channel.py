from loguru import logger
from aiogram import Router, Bot, F
from aiogram.types import ChatMemberUpdated
from aiogram.enums.chat_member_status import ChatMemberStatus


from src.infrastructure.database.uow import UnitOfWork

router = Router()


@router.my_chat_member(
    F.new_chat_member.status == ChatMemberStatus.MEMBER,
    F.new_chat_member.user.is_bot,
)
async def on_bot_added_to_channel(event: ChatMemberUpdated, uow: UnitOfWork, bot: Bot):
    async with uow:
        print(event.chat)
        channel = await uow.channel_repo.get_by_id(event.chat.id)
        if channel is None:
            channel = await uow.channel_repo.create(
                id=event.chat.id,
                name=event.chat.title,
            )
            logger.info(f"Added new channel {channel.name}: {channel.id}")

            chat_id = event.chat.linked_chat_id
            if chat_id is not None:
                chat = await bot.get_chat(chat_id)
                print(chat)
            else:
                logger.warning(
                    f"Channel {event.chat.title} ({event.chat.id}) has no linked_chat_id"
                )


@router.my_chat_member(
    F.new_chat_member.status == ChatMemberStatus.LEFT,
    F.new_chat_member.user.is_bot,
)
async def on_bot_kicked_from_channel(event: ChatMemberUpdated, uow: UnitOfWork):
    if not event.chat or not event.chat.id:
        logger.warning("No chat info in event")
        return

    async with uow:
        channel = await uow.channel_repo.get_by_id(event.chat.id)
        if channel:
            await uow.channel_repo.delete(event.chat.id)
            logger.info(f"Removed channel {event.chat.title}: {event.chat.id}")
