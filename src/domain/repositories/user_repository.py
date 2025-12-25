from abc import ABC, abstractmethod

from src.domain.models import UserDomain


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(
        self, *, id: int, username: str, is_admin: bool = False
    ) -> UserDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> UserDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: str) -> UserDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> UserDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *, id: int, username: str | None) -> UserDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[UserDomain]:
        raise NotImplementedError
