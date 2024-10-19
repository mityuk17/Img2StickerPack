from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
import texts.general as general_texts
from services.utils import remove_markups
from keyboards import GeneralInlineKeyboards

router = Router(name="General")


@router.message(Command("start"))
async def menu(message: Message):
    await message.answer(
        text=general_texts.menu(),
        reply_markup=GeneralInlineKeyboards.menu())
    

@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    
    await remove_markups(callback.message.chat.id, (await state.get_data()))
    
    await callback.message.edit_text(
        text=general_texts.menu(),
        reply_markup=GeneralInlineKeyboards.menu())