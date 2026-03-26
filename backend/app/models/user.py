from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.db.database import Base

# Stores the user information (user/admin)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin, manager, user
    created_at = Column(DateTime, default=datetime.utcnow)