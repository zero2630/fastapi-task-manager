from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services import tasks
from schemas.tasks import TaskSchema, TaskDBSchema, TaskUpdateSchema
from schemas.auth import UserRead
from db import get_async_session
from deps import get_active_user


router = APIRouter(prefix="/tasks")


CurrentUser = Annotated[UserRead, Depends(get_active_user)]


@router.post("", response_model=TaskDBSchema)
async def create_task(
    task: TaskSchema,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    current_user: Annotated[UserRead, Depends(get_active_user)],
) -> TaskDBSchema:
    task_db = await tasks.create_task(
        task=task,
        session=session,
        current_user=current_user,
    )
    return task_db


@router.get("", response_model=list[TaskDBSchema])
async def get_tasks(
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_active_user),
) -> list[TaskDBSchema]:
    tasks_response = await tasks.get_tasks(
        session=session,
        current_user=current_user,
    )
    return tasks_response


@router.get("/{task_id}", response_model=TaskDBSchema)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_active_user),
) -> TaskDBSchema:
    task_response = await tasks.get_task(
        task_id=task_id, session=session, current_user=current_user
    )
    return task_response


@router.patch("/{task_id}", response_model=TaskDBSchema)
async def update_task(
    new_task: TaskUpdateSchema,
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_active_user),
) -> TaskDBSchema:
    updated_task = await tasks.update_task(
        new_task=new_task,
        task_id=task_id,
        session=session,
        current_user=current_user,
    )
    return updated_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_active_user),
):
    await tasks.delete_task(
        task_id=task_id,
        session=session,
        current_user=current_user,
    )
    return {"status": "ok"}
