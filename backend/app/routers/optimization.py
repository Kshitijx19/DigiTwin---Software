from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.optimization_service import get_optimization_recommendations

router = APIRouter(prefix="/optimization", tags=["Optimization"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/recommendations")
def recommendations(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    return get_optimization_recommendations(db, days)