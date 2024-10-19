from aiogram.fsm.state import State, StatesGroup


class StickerPackCreation(StatesGroup):
    title = State()
    default_emoji = State()
    image = State()