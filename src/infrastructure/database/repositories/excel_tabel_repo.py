from loguru import logger
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from domain.repositories import AbstractExcelTableRepository
from database.models import ExcelTableORM
from domain.models import ExcelTableDomain


class ExcelTableRepository(AbstractExcelTableRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, id: int, sheet_id: str, sheet_url: str) -> ExcelTableDomain:
        excel_tabel_orm = ExcelTableORM(id=id, sheet_id=sheet_id, sheet_url=sheet_url)
        self.session.add(excel_tabel_orm)
        await self.session.flush()
        return excel_tabel_orm.to_domain()

    async def get_by_id(self, id: int) -> ExcelTableDomain | None:
        result = await self.session.execute(
            select(ExcelTableORM).where(ExcelTableORM.id == id)
        )
        excel_tabel_orm: ExcelTableORM | None = result.scalar_one_or_none()
        return excel_tabel_orm.to_domain() if excel_tabel_orm else None

    async def get_by_sheet_id(self, sheet_id: str) -> ExcelTableDomain | None:
        result = await self.session.execute(
            select(ExcelTableORM).where(ExcelTableORM.sheet_id == sheet_id)
        )
        excel_tabel_orm: ExcelTableORM | None = result.scalar_one_or_none()
        return excel_tabel_orm.to_domain() if excel_tabel_orm else None

    async def get_all(self) -> list[ExcelTableDomain]:
        result = await self.session.execute(select(ExcelTableDomain))
        excel_tabels_orm = result.scalars().all()
        return [excel_tabel_orm.to_domain() for excel_tabel_orm in excel_tabels_orm]

    async def delete(self, id: int) -> ExcelTableDomain | None:
        result = await self.session.execute(
            delete(ExcelTableORM).where(ExcelTableORM.id == id).returning(ExcelTableORM)
        )
        await self.session.flush()
        excel_tabel_orm: ExcelTableORM | None = result.scalar_one_or_none()
        return excel_tabel_orm.to_domain() if excel_tabel_orm else None

    async def update(
        self, *, id: int, sheet_id: str | None, sheet_url: str | None
    ) -> ExcelTableDomain | None:
        values = {}
        if sheet_id is not None:
            values["sheet_id"] = sheet_id
        if sheet_url is not None:
            values["sheet_url"] = sheet_url
        result = await self.session.execute(
            update(ExcelTableORM)
            .values(**values)
            .where(ExcelTableORM.id == id)
            .returning(ExcelTableORM)
        )
        excel_tabel_orm: ExcelTableORM | None = result.scalar_one_or_none()
        return excel_tabel_orm.to_domain() if excel_tabel_orm else None
