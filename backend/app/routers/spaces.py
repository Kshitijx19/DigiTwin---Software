import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.space import Space
from app.schemas.space import SpaceCreate, SpaceRead

router = APIRouter(prefix="/spaces", tags=["Spaces"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _derive_demo_coordinates(name: str, building: str):
    """
    Generates stable demo coordinates when latitude/longitude are not provided.
    """
    seed = f"{name}-{building}".encode("utf-8")
    digest = hashlib.md5(seed).hexdigest()

    # Campus-like demo range
    lat_base = 12.9716
    lon_base = 79.1590

    lat_offset = (int(digest[:4], 16) % 1000) / 100000
    lon_offset = (int(digest[4:8], 16) % 1000) / 100000

    latitude = round(lat_base + lat_offset, 6)
    longitude = round(lon_base + lon_offset, 6)
    return latitude, longitude


@router.post("/", response_model=SpaceRead)
def create_space(space: SpaceCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(Space)
        .filter(Space.name == space.name, Space.building == space.building)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="A space with the same name already exists in this building.",
        )

    latitude = space.latitude
    longitude = space.longitude

    if latitude is None or longitude is None:
        latitude, longitude = _derive_demo_coordinates(space.name, space.building)

    db_space = Space(
        name=space.name,
        building=space.building,
        capacity=space.capacity,
        space_type=space.space_type,
        latitude=latitude,
        longitude=longitude,
    )
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space


@router.get("/", response_model=list[SpaceRead])
def get_spaces(db: Session = Depends(get_db)):
    return db.query(Space).all()