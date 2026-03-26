from typing import Optional

from pydantic import BaseModel, ConfigDict

# Schema for the maintenance alerts
class MaintenanceAlertRead(BaseModel):
    id: int
    space_id: int
    title: str
    description: str
    severity: str
    status: str
    source: str
    resolved_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)