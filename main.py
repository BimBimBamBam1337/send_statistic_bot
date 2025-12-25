import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.types import BotCommand
from loguru import logger

from src.config import dp, bot
from src.infrastructure.database.uow import UnitOfWork
from src.infrastructure.database.engine import SessionFactory
from src.presentation.telegram.midlewares import (
    DependanciesMiddleware,
    SchedulerMiddleware,
)
from src.presentation.telegram.handlers import routers

from src.presentation.telegram.jobs import start_send_statistic


#
#
async def setup_bot_commands():
    await bot.set_my_commands(
        [
            BotCommand(command="/help", description="Информация о боте"),
            BotCommand(command="/cancel", description="Отмена действия"),
            BotCommand(command="/add_excel_tabel", description="Добавление таблицы"),
        ]
    )


async def main():
    scheduler = AsyncIOScheduler()

    # middleware

    dm = DependanciesMiddleware()
    scheduler_middleware = SchedulerMiddleware(scheduler)
    dp.message.outer_middleware(dm)
    dp.callback_query.outer_middleware(dm)
    dp.message.outer_middleware(scheduler_middleware)
    dp.callback_query.outer_middleware(scheduler_middleware)

    dp.include_routers(*routers)

    # команды бота
    await setup_bot_commands()

    # UnitOfWork
    uow = UnitOfWork(SessionFactory)

    # добавляем задачи в планировщик
    await start_send_statistic(scheduler, bot, uow)
    scheduler.start()

    # запускаем бота (блокирующий вызов)
    logger.info(f"Bot started: {await bot.get_me()}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
