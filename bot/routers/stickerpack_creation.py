from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import texts.general as general_texts
from services.stickerpack_building import sticker_pack_builder
from services import notifications, utils
from botloader import bot_loader
from database.crud.request import create_request
from schemas import StickerPackCreationRequest
from keyboards import GeneralInlineKeyboards
from states.user import StickerPackCreation
from emoji import EMOJI_DATA


router = Router(name="StickerPackCreation")


@router.callback_query(F.data == "start-creation")
async def start_creation(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(StickerPackCreation.title)
    
    message = await callback.message.edit_text(
        text=general_texts.get_title(),
        reply_markup=GeneralInlineKeyboards.cancel()
    )
    await utils.add_remove_markup_msg(message.message_id, state)
    
    
@router.message(StickerPackCreation.title)
async def get_title(message: Message, state: FSMContext):
    stickerpack_title = message.text
    
    await state.update_data({"title": stickerpack_title})
    await state.set_state(StickerPackCreation.default_emoji)
    
    message = await message.answer(
        text=general_texts.get_emoji(),
        reply_markup=GeneralInlineKeyboards.cancel()
    ) 
    
    await utils.remove_markups(message.chat.id, state)
    await utils.add_remove_markup_msg(message.message_id, state)


@router.message(StickerPackCreation.default_emoji)
async def get_default_emoji(message: Message, state: FSMContext):
    default_emoji = message.text.strip()
    if not default_emoji in EMOJI_DATA:
        return
    
    await state.update_data({"default_emoji": default_emoji})
    await state.set_state(StickerPackCreation.image)
    
    message = await message.answer(
        text=general_texts.get_image(),
        reply_markup=GeneralInlineKeyboards.cancel()
    ) 
    
    await utils.remove_markups(message.chat.id, state)
    await utils.add_remove_markup_msg(message.message_id, state)


@router.message(F.photo, StickerPackCreation.image)
async def get_photo(message: Message, state: FSMContext):
    await utils.remove_markups(message.chat.id, state)
    
    request_id = f"{message.chat.id}_{message.message_id}"
    img_save_path = f"images/given/{request_id}.png"
    await bot_loader.tg_bot.download(file=message.photo[-1].file_id, destination=img_save_path)
    
    state_data = (await state.get_data())
    request_data = StickerPackCreationRequest(
        id=request_id,
        user_id=message.from_user.id,
        title=state_data.get("title", "🐻"),
        img_path=img_save_path,
        default_emoji=state_data.get("default_emoji", "🐻")
    )
    request_id = (await create_request(request_data)).id
    await state.clear()
    try:
        stickerpack_url = await sticker_pack_builder.new_stickerpack(request_id)
        
    except:
        await message.answer(general_texts.creation_error())
        return
    
    await message.answer(general_texts.stickerpack_created(stickerpack_url))
    await notifications.new_stickerpack(request_id)