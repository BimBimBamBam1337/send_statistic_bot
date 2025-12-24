from aiogram.fsm.state import StatesGroup, State


class AddExcelTable(StatesGroup):
    URL = State()
    CHANNEL_ID = State()
