from typing import Optional

from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession
from domain.repositories import AbstractChannelRepository
from database.models import ChannelORM
from src.domain.models.chanel_model import ChannelDomain


class ChannelRepository(AbstractChannelRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, id: int, name: str) -> ChannelDomain:
        channel_orm = ChannelORM(id=id, name=name)
        self.session.add(channel_orm)
        await self.session.flush()
        return channel_orm.to_domain()

    async def get_by_id(self, id: int) -> ChannelDomain | None:
        result = await self.session.execute(
            select(ChannelORM).where(ChannelORM.id == id)
        )
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return channel_orm.to_domain() if channel_orm else None

    async def get_by_name(self, name: str) -> ChannelDomain | None:
        result = await self.session.execute(
            select(ChannelORM).where(ChannelORM.name == name)
        )
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return channel_orm.to_domain() if channel_orm else None

    async def get_all(self) -> list[ChannelDomain]:
        result = await self.session.execute(select(ChannelORM))
        channels_orm = result.scalars().all()
        return [channel_orm.to_domain() for channel_orm in channels_orm]

    async def update(self, *, id: int, name: str | None) -> ChannelDomain | None:
        values = {}
        if name is not None:
            values["name"] = name
        result = await self.session.execute(
            update(ChannelDomain)
            .values(**values)
            .where(ChannelORM.id == id)
            .returning(ChannelORM)
        )
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return channel_orm.to_domain() if channel_orm else None

    async def delete(self, id: int) -> ChannelDomain | None:
        result = await self.session.execute(
            delete(ChannelORM).where(ChannelORM.id == id).returning(ChannelORM)
        )
        await self.session.flush()
        channel_orm: ChannelORM | None = result.scalar_one_or_none()
        return channel_orm.to_domain() if channel_orm else None
