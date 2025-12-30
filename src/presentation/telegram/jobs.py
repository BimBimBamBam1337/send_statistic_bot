import asyncio
import aiohttp
from loguru import logger
from datetime import datetime
from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from src.presentation.google import (
    GoogleSheetsAsync,
)
from src.config import settings
from src.infrastructure.database.uow import UnitOfWork
from src.utils import to_date_dict
from src.presentation.telegram.utils import transform_date

gs = GoogleSheetsAsync()


API_URL = "http://194.87.134.97:8008/cheques/revenue/by-chats"


async def plan_todays_plan(bot: Bot, uow: UnitOfWork):
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
        if today_stats:
            await bot.send_message(
                chat_id=channel.id,
                text=f"""
Ваш план на сегодня:{today_stats["plan"]},
                    """,
            )
            logger.info(
                f"Отправил сообщение на {channel.id}, с названием {channel.name}"
            )


async def get_revenue_by_chats(chat_names: list[str], date: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            API_URL,
            params={"date": date},
            headers={
                "accept": "application/json",
                "x-api-key": settings.api_key,
                "Content-Type": "application/json",
            },
            json={"chat_names": chat_names},
        ) as resp:
            resp.raise_for_status()
            return await resp.json()


async def push_low_percent(bot: Bot, uow: UnitOfWork, max_percent: int):
    month = transform_date(datetime.today().month)
    date_str = datetime.today().strftime("%d.%m")
    api_date = datetime.today().strftime("%d.%m.%Y")

    async with uow:
        excel_tables = await uow.excel_tabel_repo.get_all()

    chat_names = [table.channel.name for table in excel_tables if table.channel]

    revenue_map = await get_revenue_by_chats(chat_names, api_date)

    for table in excel_tables:
        channel = table.channel
        if not channel:
            continue

        raw_data = await gs.get_statistic(table.sheet_id, month)
        stats = to_date_dict(raw_data)

        today_stats = stats.get(date_str)
        if not today_stats or today_stats["plan"] is None:
            continue

        revenue = revenue_map.get(channel.name, {}).get("total_revenue", 0)
        plan = today_stats["plan"]

        if plan <= 0:
            continue

        percent = int((revenue / plan) * 100)

        if percent < max_percent:
            await bot.send_message(
                chat_id=channel.id,
                text=(f"План на сегодня: {plan}\n" f"Выполнено: {percent}%"),
            )
            logger.info(
                f"Отправил сообщение на {channel.id}, с названием {channel.name}, таблица привязанная: {table.sheet_id}"
            )


async def start_send_statistic(scheduler, bot: Bot, uow: UnitOfWork):
    scheduler.add_job(
        plan_todays_plan,
        CronTrigger(hour=8, minute=0),
        kwargs={"bot": bot, "uow": uow},
        id="push_8",
    )
    scheduler.add_job(
        push_low_percent,
        CronTrigger(hour=12, minute=0),
        kwargs={"bot": bot, "uow": uow, "max_percent": 20},
        id="push_12",
    )
    scheduler.add_job(
        push_low_percent,
        CronTrigger(hour=13, minute=0),
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
