from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    status: Literal["active", "completed", "archived", "paused"] | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)