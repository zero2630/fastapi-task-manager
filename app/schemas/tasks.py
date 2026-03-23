from pydantic import BaseModel, Field, ConfigDict

from app.schemas.auth import UserRead


class TaskSchema(BaseModel):
    title: str = Field(max_length=64, description="Task main info")
    description: str = Field(default="")


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(default=None, max_length=64, description="Task main info")
    description: str | None = Field(default=None)


class TaskDBSchema(TaskSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user: UserRead
