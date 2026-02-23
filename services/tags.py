from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from models.tasks_tags import TagModel
from schemas.tags import TagDBSchema, TagSchema


async def create_tag(tag: TagSchema, session: AsyncSession):
    db_tag = TagModel(
        name=tag.name,
    )
    try:
        session.add(db_tag)
        await session.flush()
        return TagDBSchema.model_validate(db_tag)
    except IntegrityError as e:
        if isinstance(getattr(e.orig, "__cause__", None), UniqueViolationError):
            raise HTTPException(
                status_code=409,
                detail="Tag with this name already exists",
            )
        raise HTTPException(status_code=500)


async def delete_tag(tag_id: int, session: AsyncSession):
    tag = await session.get(TagModel, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag with this id doesn't exist")

    await session.delete(tag)
    return True


async def get_tags(session: AsyncSession):
    tags = await session.scalars(select(TagModel).order_by(TagModel.id))
    return [TagDBSchema.model_validate(tag) for tag in tags]


async def get_tag(tag_id: int, session: AsyncSession):
    tag = await session.get(TagModel, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag with this id doesn't exist")

    return TagDBSchema.model_validate(tag)
