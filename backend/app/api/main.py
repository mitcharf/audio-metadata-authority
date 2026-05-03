from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.models.mediafile import MediaFile
from app.utils.tag_maps import friendly_name
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Dependency
def get_session():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        session.close()

class MediaTagOut(BaseModel):
    tag: str
    display_name: str
    value: str
    class Config:
        orm_mode = True

class MediaFileOut(BaseModel):
    id: int
    path: str
    tags: List[MediaTagOut]
    class Config:
        orm_mode = True

@router.get("/files/", response_model=List[MediaFileOut])
async def list_files(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        MediaFile.__table__.select()
    )
    files = result.fetchall()
    file_objs = []
    for row in files:
        media_file = row
        tags_result = await session.execute(
            f"SELECT tag, value FROM media_tags WHERE file_id = {media_file.id}"
        )
        tags = [
            MediaTagOut(
                tag=tag_row[0],
                display_name=friendly_name(tag_row[0]),
                value=tag_row[1]
            ) for tag_row in tags_result.fetchall()
        ]
        file_objs.append(MediaFileOut(id=media_file.id, path=media_file.path, tags=tags))
    return file_objs
