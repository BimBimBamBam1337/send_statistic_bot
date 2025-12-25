from abc import ABC, abstractmethod

from src.domain.models import ExcelTableDomain


class AbstractExcelTableRepository(ABC):
    @abstractmethod
    async def create(
        self, sheet_id: str, sheet_url: str, name: str
    ) -> ExcelTableDomain:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> ExcelTableDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_sheet_id(self, sheet_id: str) -> ExcelTableDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> ExcelTableDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, *, id: int, sheet_id: str | None, sheet_url: str | None
    ) -> ExcelTableDomain | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[ExcelTableDomain]:
        raise NotImplementedError
