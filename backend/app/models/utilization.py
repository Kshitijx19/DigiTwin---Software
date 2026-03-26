from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String

from app.db.database import Base

# Stores about the Utilisation costs of the spaces
class Utilization(Base):
    __tablename__ = "utilization_records"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False, index=True)
    record_date = Column(Date, nullable=False, index=True)
    time_slot = Column(String(50), nullable=False)
    scheduled_users = Column(Integer, nullable=False)
    actual_users = Column(Integer, nullable=False)
    duration_hours = Column(Integer, nullable=False, default=2)
    source = Column(String(50), nullable=False, default="simulated")
    created_at = Column(DateTime, default=datetime.utcnow)