from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WorkItemCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(
        default=None,
        max_length=5000
    )
    priority: Literal["low", "medium", "high"] = "medium"


class WorkItemUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    description: str | None = Field(
        default=None,
        max_length=5000
    )
    status: Literal["todo", "in_progress", "done"] | None = None
    priority: Literal["low", "medium", "high"] | None = None


class WorkItemResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: str
    priority: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)