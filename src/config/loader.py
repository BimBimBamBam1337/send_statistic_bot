from aiogram import Bot, Dispatcher

from . import settings

__all__ = ["bot", "dp"]


bot = Bot(settings.token)
dp = Dispatcher()
