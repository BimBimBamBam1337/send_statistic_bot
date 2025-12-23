from typing import Optional

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database.models import Chanel


class ChannelRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, channel_id: int, title: str) -> Chanel:
        channel = Chanel(id=channel_id, title=title)
        self.session.add(channel)
        await self.session.flush()
        return channel

    async def get(self, channel_id: int) -> Chanel | None:
        channel = await self.session.get(Chanel, channel_id)
        return channel

    async def get_by_title(self, title: str) -> Chanel | None:
        result = await self.session.execute(select(Chanel).where(Chanel.title == title))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Chanel]:
        result = await self.session.execute(select(Chanel))
        channels = result.scalars().all()
        return list(channels)

    async def delete(self, channel_id: int):
        await self.session.execute(delete(Chanel).where(Chanel.id == channel_id))
        await self.session.flush()
