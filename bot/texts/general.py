from html import escape
from schemas import StickerPackCreationRequest
from services.utils import build_stickerpack_url


def menu() -> str:
    text = "Выберите действие"
    
    return text


def get_title() -> str:
    text = "Пришлите название для стикерпака"
    
    return text


def get_emoji() -> str:
    text = "Пришлите эмоджи для стикеров"
    
    return text


def get_image() -> str:
    text = "Пришлите изображение"
    
    return text


def stickerpack_created(stickerpack_url: str) -> str:
    text = f"""<b>Стикерпак создан.</b>
<i>Ссылка:</i> {escape(stickerpack_url)}"""
    
    return text


def stickerpack_info(stickerpack_data: StickerPackCreationRequest) -> str:
    text = f"""<b>стикерпак {stickerpack_data.id}</b>
<i>Назание:</i> {escape(stickerpack_data.title)}
<i>Ссылка:</i> {escape(build_stickerpack_url(stickerpack_data))}"""

    return text


def new_stickerpack_notification(stickerpack_data: StickerPackCreationRequest) -> str:
    text = f"""<b>Новый стикерпак</b>
<i>Id запроса:</i> {stickerpack_data.id}
<i>Id пользователя:</i> {stickerpack_data.user_id}
<i>Назание:</i> {escape(stickerpack_data.title)}
<i>Ссылка:</i> {escape(build_stickerpack_url(stickerpack_data))}"""

    return text


def creation_error() -> str:
    text = "❗️При создание стикерпака произошла ошибка"
    
    return text