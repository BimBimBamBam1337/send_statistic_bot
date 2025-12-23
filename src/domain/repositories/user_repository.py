from abc import ABC, abstractmethod

from domain.models import UserDomain


class AbstractUserRepository(ABC):
    @abstractmethod
    async def exists(self, sheet_id: str) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *, id: int, username: str) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_sheet_id(self, sheet_id: str) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *, id: int, username: str | None) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[UserDomain]:
        raise NotImplementedError
