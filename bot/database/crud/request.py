from botloader import bot_loader
from schemas import StickerPackCreationRequest
from sqlmodel import select


async def create_request(request_data: StickerPackCreationRequest) -> StickerPackCreationRequest:
    session = await bot_loader.database_manager.get_session()
    
    session.add(request_data)
    await session.commit()
    await session.refresh(request_data)
    await session.close()
    
    return request_data


async def get_request(request_id: str) -> StickerPackCreationRequest | None:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(StickerPackCreationRequest).where(StickerPackCreationRequest.id == request_id)
    result = await session.exec(statement)
    request = result.one_or_none()
    await session.close()
    
    return request


async def update_request(request_data: StickerPackCreationRequest) -> StickerPackCreationRequest:
    session = await bot_loader.database_manager.get_session()
    
    session.add(request_data)
    await session.commit()
    await session.close()
    
    return request_data


async def get_user_requests(user_id: int, offset: int=0, limit:int=None,only_successful: bool=True) -> list[StickerPackCreationRequest]:
    session = await bot_loader.database_manager.get_session()
    
    statement = select(StickerPackCreationRequest).where(StickerPackCreationRequest.user_id == user_id)
    if only_successful:
        statement = statement.where(StickerPackCreationRequest.successful == True)
    statement = statement.offset(offset).limit(limit)
    result = await session.exec(statement)
    requests = result.all()
    await session.close()
    
    return requests