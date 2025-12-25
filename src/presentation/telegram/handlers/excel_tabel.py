from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext

from src.presentation.google import GoogleSheetsAsync
from src.presentation.telegram.filters import AdminFilter
from src.infrastructure.database.uow import UnitOfWork
from src.presentation.telegram import texts
from src.presentation.telegram.states import AddExcelTable
from src.presentation.telegram.constans import GOOGLE_SHEET_RE

router = Router()


@router.message(Command("add_excel_tabel"), AdminFilter())
async def add_excel_tabel(message: Message, state: FSMContext, uow: UnitOfWork):
    await message.answer(text=texts.msg_add_excel_tabel)
    await state.set_state(AddExcelTable.URL)


@router.message(F.text, AddExcelTable.URL)
async def parse_sheet_id(
    message: Message,
    state: FSMContext,
):
    text = message.text.strip()

    match = GOOGLE_SHEET_RE.search(text)
    if not match:
        await message.answer(
            "Это не ссылка на Google таблицу. Пришли корректную ссылку."
        )
        return

    sheet_id = match.group(1)

    await state.update_data(sheet_id=sheet_id, sheet_url=text)
    await message.answer(text=texts.msg_send_channel_id)
    await state.set_state(AddExcelTable.CHANNEL_ID)


@router.message(AddExcelTable.CHANNEL_ID)
async def create_channel_and_tabel(
    message: Message,
    state: FSMContext,
    google_sheet: GoogleSheetsAsync,
    uow: UnitOfWork,
):
    data = await state.get_data()

    sheet_id: str = data["sheet_id"]
    sheet_url: str = data["sheet_url"]

    channel_id = int(message.text.strip())

    spreadsheet = await google_sheet.get_sheet(sheet_id)

    async with uow:
        table = await uow.excel_tabel_repo.get_by_sheet_id(sheet_id)
        if not table:
            table = await uow.excel_tabel_repo.create(
                sheet_id=sheet_id,
                sheet_url=sheet_url,
                name=spreadsheet.title,
            )
            print(table)
            channel = await uow.channel_repo.get_by_id(channel_id)
            if not channel and table:
                channel = await uow.channel_repo.create(
                    id=channel_id, name=spreadsheet.title, sheet_id=sheet_id
                )

    await state.clear()
    await message.answer("Таблица успешно привязана к каналу ✅")
