from botloader import bot_loader
from schemas import StickerPackCreationRequest
from database.crud.request import get_request
from config import config
from texts import general as general_texts


async def new_stickerpack(request_id: str):
    request_data = await get_request(request_id)
    
    await bot_loader.tg_bot.send_message(
        chat_id=config.ADMIN_CHAT_ID,
        text=general_texts.new_stickerpack_notification(request_data)
    )