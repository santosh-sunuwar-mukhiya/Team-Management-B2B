import uuid
from enum import Enum
from datetime import datetime
from typing import Optional
import sqlalchemy as sa  # type: ignore
from sqlmodel import SQLModel, Field  # type: ignore


class TaskStatus(str, Enum):
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"


class Task(SQLModel, table=True):  # type: ignore
    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,  # Python-side UUID generation
        primary_key=True,
        sa_type=sa.UUID(as_uuid=True),  # native UUID column in DB
    )
    title: str
    description: Optional[str] = None  # no need for Field() just for None default
    status: TaskStatus = TaskStatus.PENDING
    org_id: str = Field(index=True)
    created_by: str

    created_at: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),  # DB sets this on INSERT
            nullable=False,
        )
    )
    updated_at: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),  # DB sets on INSERT
            onupdate=sa.func.now(),  # DB auto-updates on every UPDATE ✅
            nullable=False,
        )
    )
