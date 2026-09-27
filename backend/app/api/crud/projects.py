from fastapi import APIRouter, Depends, HTTPException, status
from app.models.project import Project
from sqlalchemy.orm import Session

def get_project_or_404(project_id: int, db: Session) -> Project:
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project