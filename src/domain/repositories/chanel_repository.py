from abc import ABC, abstractmethod

from src.domain.models import ChannelDomain


class AbstractChannelRepository(ABC):
    @abstractmethod
    async def create(self, id: int, name: str, sheet_id: str) -> ChannelDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> ChannelDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> ChannelDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> ChannelDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *, id: int, name: str | None) -> ChannelDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[ChannelDomain]:
        raise NotImplementedError
