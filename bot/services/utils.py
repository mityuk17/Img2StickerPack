from aiogram.fsm.context import FSMContext
from botloader import bot_loader
from schemas import StickerPackCreationRequest
from config import config


async def add_remove_markup_msg(msg_id: int, state: FSMContext):
    state_data = await state.get_data()
    remove_reply_markup = state_data.get("remove_reply_markup", []) + [msg_id]
    await state.update_data({"remove_reply_markup": remove_reply_markup})

async def remove_markups(chat_id: int, state: FSMContext):
    state_data = await state.get_data()
    for msg_id in state_data.get("remove_reply_markup", []):
        await bot_loader.tg_bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=None
        )
    await state.update_data({"remove_reply_markup": []})
    
    
def build_stickerpack_name(stickerpack_data: StickerPackCreationRequest) -> str:
    stickerpack_name = f"s_{stickerpack_data.id}_by_{config.TELEGRAM_BOT_USERNAME}"
    
    return stickerpack_name
    
    
def build_stickerpack_url(stickerpack_data: StickerPackCreationRequest) -> str:
    stickerpack_url = f"t.me/addstickers/{build_stickerpack_name(stickerpack_data)}"
    
    return stickerpack_url