from loguru import logger
from aiogram import Router, F, types
from aiogram.filters import CommandStart

from src.telegram.filters import AdminFilter

from src.infrastructure.database.uow import UnitOfWork

router = Router()


@router.message(CommandStart(), AdminFilter())
async def start(message: types.Message, uow: UnitOfWork):
    """Регистрация пользователя"""
    async with uow:
        user_exist = await uow.user_repo.get(message.from_user.id)  # type:ignore
        if user_exist is None:
            user = await uow.user_repo.create(
                id=message.from_user.id,
                username=message.from_user.username,
                is_admin=True,
            )  # type: ignore
            logger.info(f"Registrate user {user.id}")

    await message.answer(
        text="""
<b>Добро пожаловать!</b> 🎉

Вы используете бота для рассылок в каналы.

Чтобы отправить сообщение в нужный канал:
— Укажите <b>точное имя канала</b>, как оно указано в Telegram.
— Например, если канал называется <code>ТЕСТ</code>, нужно написать именно <code>ТЕСТ</code> — без лишних символов и пробелов.

Для этого напишите: /newsletter
""",
        parse_mode="HTML",
    )
