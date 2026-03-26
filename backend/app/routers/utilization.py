from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.analytics_service import (
    generate_demo_utilization_records,
    get_space_utilization_summary,
)

router = APIRouter(prefix="/utilization", tags=["Utilization"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/seed/{space_id}")
def seed_utilization(
    space_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    try:
        return generate_demo_utilization_records(db, space_id, days)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/summary/{space_id}")
def utilization_summary(
    space_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    try:
        return get_space_utilization_summary(db, space_id, days)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))