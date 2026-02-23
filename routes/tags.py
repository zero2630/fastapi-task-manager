from fastapi import APIRouter, Depends


from services import tags
from schemas.tags import TagSchema, TagDBSchema
from db import get_async_session


router = APIRouter(prefix="/tags")


@router.post("", response_model=TagDBSchema)
async def create_tag(
    tag: TagSchema,
    session=Depends(get_async_session),
) -> TagDBSchema:
    return await tags.create_tag(tag, session)


@router.get("", response_model=list[TagDBSchema])
async def get_tags(
    session=Depends(get_async_session),
) -> list[TagDBSchema]:
    return await tags.get_tags(session)


@router.get("/{tag_id}", response_model=TagDBSchema)
async def get_tag(
    tag_id: int,
    session=Depends(get_async_session),
) -> TagDBSchema:
    return await tags.get_tag(tag_id, session)


@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    session=Depends(get_async_session),
):
    await tags.delete_tag(tag_id, session)
    return {"status": "ok"}
