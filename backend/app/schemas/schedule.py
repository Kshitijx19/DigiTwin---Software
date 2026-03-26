from pydantic import BaseModel, ConfigDict

# Schema for the Schedules
class ScheduleCreate(BaseModel):
    space_id: int
    course_name: str
    department: str
    day_of_week: str
    start_time: str
    end_time: str
    expected_attendees: int


class ScheduleRead(ScheduleCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)