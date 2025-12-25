import asyncio
from datetime import datetime
from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from src.presentation.google import (
    GoogleSheetsAsync,
)
from src.infrastructure.database.uow import UnitOfWork
from src.utils import to_date_dict
from src.presentation.telegram.utils import transform_date

gs = GoogleSheetsAsync()


async def push_low_percent(bot: Bot, uow: UnitOfWork, max_percent: int):
    month = transform_date(datetime.today().month)
    date = datetime.today().strftime("%d.%m")
    async with uow:
        excel_tables = await uow.excel_tabel_repo.get_all()

    for table in excel_tables:
        channel = table.channel
        if not channel:
            continue

        raw_data = await gs.get_statistic(table.sheet_id, month)
        stats = to_date_dict(raw_data)

        today_stats = stats.get(date)
        if not today_stats or today_stats["percent"] is None:
            continue
        if today_stats["percent"] < max_percent:
            await bot.send_message(
                chat_id=-1 * channel.id,
                text=f"""
    План на сегодня:{today_stats["plan"]},
    Выполнен на: {today_stats["percent"]}
                    """,
            )


async def start_send_statistic(scheduler, bot: Bot, uow: UnitOfWork):
    scheduler.add_job(
        push_low_percent,
        CronTrigger(hour=12, minute=0),
        kwargs={"bot": bot, "uow": uow, "max_percent": 20},
        id="push_12",
    )
    scheduler.add_job(
        push_low_percent,
        CronTrigger(hour=15, minute=0),
        kwargs={"bot": bot, "uow": uow, "max_percent": 40},
        id="push_15",
    )
    scheduler.add_job(
        push_low_percent,
        CronTrigger(hour=18, minute=0),
        kwargs={"bot": bot, "uow": uow, "max_percent": 60},
        id="push_18",
    )
    scheduler.add_job(
        push_low_percent,
        CronTrigger(hour=22, minute=12),
        kwargs={"bot": bot, "uow": uow, "max_percent": 75},
        id="push_21",
    )
