from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas.tasks import TaskSchema, TaskDBSchema, TaskUpdateSchema
from schemas.auth import UserRead
from models.tasks_tags import TaskModel, TagModel


def check_owner(user_id: int, task_user_id: int):
    if user_id != task_user_id:
        raise HTTPException(status_code=403, detail="Task owned by another user")


async def create_task(
    task: TaskSchema,
    session: AsyncSession,
    current_user: UserRead,
):
    task_db = TaskModel(
        title=task.title, description=task.description, user_id=current_user.id
    )
    session.add(task_db)
    await session.flush()

    await session.refresh(task_db, attribute_names=["tags", "user"])

    return TaskDBSchema.model_validate(task_db)


async def get_tasks(
    session: AsyncSession,
    current_user: UserRead,
):
    db_tasks = await session.scalars(
        select(TaskModel).filter_by(user_id=current_user.id).order_by(TaskModel.id)
    )
    tasks = [TaskDBSchema.model_validate(db_task) for db_task in db_tasks]
    return tasks


async def get_task(
    task_id: int,
    session: AsyncSession,
    current_user: UserRead,
):
    db_task = await session.get(TaskModel, task_id)
    if db_task:
        check_owner(current_user.id, db_task.user_id)
        return TaskDBSchema.model_validate(db_task)

    raise HTTPException(status_code=404, detail="Task with this id doesn't exists")


async def delete_task(
    task_id: int,
    session: AsyncSession,
    current_user: UserRead,
):
    db_task = await session.get(TaskModel, task_id)
    if db_task:
        check_owner(current_user.id, db_task.user_id)

        await session.delete(db_task)
        return True

    raise HTTPException(status_code=404, detail="Task with this id doesn't exists")


async def update_task(
    new_task: TaskUpdateSchema,
    task_id: int,
    session: AsyncSession,
    current_user: UserRead,
):
    db_task = await session.get(TaskModel, task_id)
    if db_task:
        check_owner(current_user.id, db_task.user_id)

        if new_task.title is not None:
            db_task.title = new_task.title
        if new_task.description is not None:
            db_task.description = new_task.description
        if new_task.tags is not None:
            stmt = select(TagModel).where(TagModel.id.in_(new_task.tags))
            tags = await session.scalars(stmt)
            db_task.tags = []
            for tag in tags:
                db_task.tags.append(tag)

        await session.flush()
        await session.refresh(db_task, attribute_names=["tags"])
        return TaskDBSchema.model_validate(db_task)

    raise HTTPException(status_code=404, detail="Task with this id doesn't exists")
