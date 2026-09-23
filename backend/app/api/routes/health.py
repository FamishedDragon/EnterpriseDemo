from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/database")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {"database_status": "ok"}

@router.get("/backend")
def backend_health():
    return {"backend_status": "ok"}