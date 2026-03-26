from fastapi import APIRouter, Response
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.space import Space

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/spaces")
def export_spaces():
    db: Session = next(get_db())

    spaces = db.query(Space).all()

    csv = "id,name,building,capacity,type\n"

    for s in spaces:
        csv += f"{s.id},{s.name},{s.building},{s.capacity},{s.space_type}\n"

    return Response(
        content=csv,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=spaces.csv"},
    )