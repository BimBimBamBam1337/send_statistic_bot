from abc import ABC, abstractmethod

from domain.models import ChanelDomain


class AbstractChanelRepository(ABC):
    @abstractmethod
    async def exists(self, id: int) -> ChanelDomain:
        raise NotImplementedError

    @abstractmethod
    async def create(self, id: int, name: str) -> ChanelDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> ChanelDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> ChanelDomain:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> ChanelDomain:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *, id: int, name: str | None) -> ChanelDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[ChanelDomain]:
        raise NotImplementedError
