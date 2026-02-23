from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Table, Column, ForeignKey, String, Text

from models.base import Base

TaskTag = Table(
    "tasks_tags",
    Base.metadata,
    Column(
        "task_id",
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "tag_id",
        ForeignKey(
            "tags.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    ),
)


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    tags: Mapped[list["TagModel"]] = relationship(
        "TagModel", secondary=TaskTag, back_populates="tasks", lazy="selectin"
    )
    user: Mapped["User"] = relationship(
        "UserModel", back_populates="tasks", lazy="selectin"
    )


class TagModel(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel", secondary=TaskTag, back_populates="tags", lazy="selectin"
    )
