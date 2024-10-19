from aiogram import Router, F
from aiogram.types import InlineQuery, Message, InlineQueryResultArticle, InputTextMessageContent
import texts.general as general_texts
from database.crud.request import get_user_requests, get_request
import re


router = Router(name="StickerPackManagement")


@router.inline_query(F.query.strip() == "Мои стикерпаки")
async def show_user_stickerpacks(query: InlineQuery):
    offset = int(query.offset or 0)
    stickerpacks = await get_user_requests(query.from_user.id, offset=offset, limit=50)
    
    answer = []
    for pack in stickerpacks:
        answer.append(InlineQueryResultArticle(
            id=pack.id,
            title=pack.title,
            input_message_content=InputTextMessageContent(message_text=f"/pack {pack.id}")
        ))
    
    await query.answer(
        results=answer,
        cache_time=30,
        is_personal=True,
        next_offset=str(offset+50),
    )


@router.message(F.text.startswith("/pack"))
async def show_stickerpack(message: Message):
    stickerpack_id = message.text.split()[-1].strip()
    if not(re.fullmatch(pattern=r"-?\d+_\d+", string=stickerpack_id)):
        return
    
    request = await get_request(stickerpack_id)
    
    await message.reply(general_texts.stickerpack_info(request))
    
