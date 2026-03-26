from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.maintenance_service import (
    generate_maintenance_alerts,
    get_all_maintenance_alerts,
)

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/scan")
def scan_maintenance(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    return generate_maintenance_alerts(db, days)


@router.get("/")
def list_maintenance_alerts(db: Session = Depends(get_db)):
    return get_all_maintenance_alerts(db)