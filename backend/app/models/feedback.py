from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text

from app.db.database import Base

# Stores the variable information for the feedback 
class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False, index=True)
    user_name = Column(String(100), nullable=False)
    issue_type = Column(String(80), nullable=False)
    message = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    distance_meters = Column(Float, nullable=False)
    geofence_status = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)