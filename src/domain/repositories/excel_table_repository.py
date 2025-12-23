from abc import ABC, abstractmethod

from domain.models import ExcelTableDomain


class AbstractExcelTableRepository(ABC):
    @abstractmethod
    async def exists(self, sheet_id: str) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def create(self, id: int, sheet_id: str, sheet_url: str) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_sheet_id(self, sheet_id: str) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, *, id: int, sheet_id: str | None, sheet_url: str | None
    ) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[ExcelTableDomain]:
        raise NotImplementedError
