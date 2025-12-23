from aiogram.fsm.state import StatesGroup, State


class Newsletter(StatesGroup):
    Title = State()
    Text = State()
