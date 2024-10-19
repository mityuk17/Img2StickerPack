from services.image_processing import ImageProcessor
from schemas import StickerPackCreationRequest
from aiogram import Bot
from aiogram.types.input_sticker import InputSticker
from aiogram.types.input_file import FSInputFile
from botloader import bot_loader
import os
from database.crud.request import get_request, update_request
from services.utils import build_stickerpack_name, build_stickerpack_url


class StickerPackBuilder:
    def __init__(self, tg_bot: Bot):
        self.tg_bot = tg_bot
        if not os.path.exists("./images"): os.mkdir("images")
        if not os.path.exists("./images/given"): os.mkdir("images/given")
        if not os.path.exists("./images/processed"): os.mkdir("images/processed")
        
        
    async def new_stickerpack(self, requet_id: str):
        request = await get_request(requet_id)
        stickers = []
        stickers_imgs = self.process_img(request)
        for img in stickers_imgs:
            sticker = InputSticker(
                sticker=FSInputFile(img),
                format="static",
                emoji_list=[request.default_emoji]
            )
            stickers.append(sticker)
        
        stickerpack_name = build_stickerpack_name(request)
        
        result = await self.tg_bot.create_new_sticker_set(
            user_id=request.user_id,
            name=stickerpack_name,
            title=request.title,
            stickers=stickers,
        )
        
        if not result:
            raise Exception()
        
        request.successful = True
        await update_request(request)
        sticker_pack_url = build_stickerpack_url(request)
        
        return sticker_pack_url
    
    
    def process_img(self, request: StickerPackCreationRequest) -> list[str]:
        img_processor = ImageProcessor(request.img_path)
        files = img_processor.get_cut_image(request.id)
        
        return files
    

sticker_pack_builder = StickerPackBuilder(bot_loader.tg_bot)