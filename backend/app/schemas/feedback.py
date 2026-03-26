from pydantic import BaseModel, ConfigDict

# Schema for the feedback
class FeedbackCreate(BaseModel):
    space_id: int
    user_name: str
    issue_type: str
    message: str
    latitude: float
    longitude: float


class FeedbackRead(FeedbackCreate):
    id: int
    distance_meters: float
    geofence_status: str

    model_config = ConfigDict(from_attributes=True)