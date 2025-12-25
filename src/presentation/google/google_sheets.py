import gspread

from loguru import logger
from gspread_asyncio import (
    AsyncioGspreadClientManager,
    AsyncioGspreadWorksheet,
    AsyncioGspreadSpreadsheet,
)
from google.oauth2.service_account import Credentials


def get_creds():
    return Credentials.from_service_account_file(
        "credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )


class GoogleSheetsAsync:
    def __init__(self):
        try:
            self.agcm = AsyncioGspreadClientManager(get_creds)
        except Exception as e:
            logger.error(f"Ошибка при инициализации GoogleSheets: {e}", extra="google")
            raise

    async def get_sheet(self, sheet_id: str) -> AsyncioGspreadSpreadsheet:
        try:
            agc = await self.agcm.authorize()
            sheet = await agc.open_by_key(sheet_id)
            return sheet
        except gspread.WorksheetNotFound:
            logger.error(f"Не найдена таблица с id {sheet_id}")

    async def get_sheet_date(
        self, sh, title: str, sheet_id: str
    ) -> AsyncioGspreadWorksheet:
        """Получить лист по названию или создать с заголовками"""
        try:
            worksheet = await sh.worksheet(title)
            return worksheet
        except gspread.WorksheetNotFound:
            logger.error(f"Не найден лист: {title} sheet_id {sheet_id}")

    async def get_statistic(self, sheet_id: str, sheet_title: str) -> list[list[str]]:
        """Выводит статистику по номеру за месяц"""
        try:
            agc = await self.agcm.authorize()
            sh = await agc.open_by_key(sheet_id)
            worksheet = await self.get_sheet_date(sh, sheet_title, sheet_id)

            rows = await worksheet.get_all_values()
            result: list[list[str]] = []

            for row in rows[2:10]:
                cleaned_row: list[str] = []
                i = 0

                while i < len(row):
                    cell = row[i].strip()

                    if cell and cell[0].isdigit() and "." in cell:
                        date_ = cell
                        plan = row[i + 1].strip() if i + 1 < len(row) else ""
                        fact = row[i + 2].strip() if i + 2 < len(row) else ""
                        percent = row[i + 3].strip() if i + 3 < len(row) else ""

                        cleaned_row.extend([date_, plan, fact, percent])
                        i += 4
                    else:
                        i += 1

                if cleaned_row:
                    result.append(cleaned_row)

            return result
        except Exception as e:
            logger.error("Возникла ошибка {}", e)
