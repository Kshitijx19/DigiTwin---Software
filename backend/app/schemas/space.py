from typing import Optional

from pydantic import BaseModel, ConfigDict

# Schema for the Spaces creation and reading
class SpaceCreate(BaseModel):
    name: str
    building: str
    capacity: int
    space_type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SpaceRead(BaseModel):
    id: int
    name: str
    building: str
    capacity: int
    space_type: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)