from datetime import date

from pydantic import BaseModel, ConfigDict

# Schema for the Utilisation checked
class UtilizationCreate(BaseModel):
    space_id: int
    record_date: date
    time_slot: str
    scheduled_users: int
    actual_users: int
    duration_hours: int = 2
    source: str = "simulated"


class UtilizationRead(UtilizationCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)