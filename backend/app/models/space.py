from sqlalchemy import Column, Float, Integer, String

from app.db.database import Base

# Stores the information about the spaces
class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    building = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    space_type = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)