from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.models.work_item import WorkItem
from app.schemas.work_item import (
    WorkItemCreate,
    WorkItemResponse,
)
from app.api.crud.projects import get_project_or_404

router = APIRouter(
    prefix="/work-items",
    tags=["Work Items"]
)

@router.post(
    "",
    response_model=WorkItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_work_item(
    work_item_data: WorkItemCreate,
    db: Session = Depends(get_db)
):
    project = get_project_or_404(work_item_data.project_id, db)

    work_item = WorkItem(
        project_id=work_item_data.project_id,
        title=work_item_data.title,
        description=work_item_data.description,
        priority=work_item_data.priority
    )

    db.add(work_item)
    db.commit()
    db.refresh(work_item)

    return work_item

@router.get(
    "/project/{project_id}",
    response_model=list[WorkItemResponse]
)
def list_work_items(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = get_project_or_404(project_id, db)

    statement = (
        select(WorkItem)
        .where(WorkItem.project_id == project_id)
        .order_by(WorkItem.id)
    )

    return db.scalars(statement).all()

@router.get(
    "/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):
    work_item = db.get(WorkItem, work_item_id)

    if work_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found"
        )

    return work_item