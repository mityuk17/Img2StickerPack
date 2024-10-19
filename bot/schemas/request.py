from sqlmodel import SQLModel, Field
from sqlalchemy import Column, BigInteger, ForeignKey
from datetime import datetime


class StickerPackCreationRequest(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: int = Field(sa_column=Column(BigInteger(), ForeignKey("user.id")))
    title: str
    img_path: str
    default_emoji: str
    successful: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now())
    