from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Создать стикерпак", callback_data="start-creation"),
    kb.button(text="Мои стикерпаки", switch_inline_query_current_chat="Мои стикерпаки")
    
    kb.adjust(1, repeat=True)
    
    return kb.as_markup()


def cancel() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(text="Отмена", callback_data="menu")
    
    return kb.as_markup()