"""
Feedback & Maintenance Module

This module handles:
1. User feedback submission for a specific space.
2. Geofencing validation (ensuring user is physically near the space).
3. Automatic detection of maintenance-related issues from feedback.
4. Creation of maintenance alerts for facility management.

Key Features:
- Uses Haversine formula to calculate real-world distance.
- Restricts feedback submission within a defined radius.
- Classifies maintenance issues and assigns severity.
- Automatically logs alerts for actionable issues.
"""

from math import radians, sin, cos, sqrt, atan2
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.feedback import Feedback
from app.models.maintenance import MaintenanceAlert
from app.models.space import Space


def haversine_distance_m(lat1, lon1, lat2, lon2):
    """Utility function to calculate distance (in meters) between two coordinates."""
    r = 6371000
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c


def _maintenance_severity(issue_type: str, message: str) -> str:
    """Determines severity level (High/Medium) of a maintenance issue."""
    issue_type = (issue_type or "").lower()
    message = (message or "").lower()

    if any(word in issue_type for word in ["electrical", "projector", "ac"]) or any(
        word in message for word in ["not working", "broken", "failed", "damage", "smoke"]
    ):
        return "High"

    if any(word in issue_type for word in ["furniture", "cleanliness", "general"]):
        return "Medium"

    return "Medium"


def _is_maintenance_issue(issue_type: str, message: str) -> bool:
    """Checks whether feedback corresponds to a maintenance-related issue."""
    text = f"{issue_type} {message}".lower()

    maintenance_keywords = [
        "chair", "table", "desk", "broken", "damage", "damaged",
        "projector", "ac", "air conditioner", "fan", "light",
        "electrical", "plug", "socket", "clean", "dirty", "leak",
        "ceiling", "window", "door", "lock", "bench",
        "furniture", "whiteboard", "speaker",
    ]

    return any(keyword in text for keyword in maintenance_keywords)


def submit_feedback(db: Session, payload, radius_meters: int = 100):
    """
    API Logic: Submit Feedback

    Workflow:
    1. Validate the space exists and has location data.
    2. Compute distance between user and space using geolocation.
    3. Enforce geofencing (user must be within allowed radius).
    4. Store feedback in the database.
    5. Detect if feedback indicates a maintenance issue.
    6. If yes, create a maintenance alert with severity.

    Returns:
    - Saved feedback object

    Raises:
    - 404 if space not found
    - 400 if outside geofence or missing location data
    """

    space = db.query(Space).filter(Space.id == payload.space_id).first()
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    if space.latitude is None or space.longitude is None:
        raise HTTPException(status_code=400, detail="Space does not have location data")

    distance = haversine_distance_m(
        payload.latitude,
        payload.longitude,
        space.latitude,
        space.longitude,
    )

    geofence_status = "within_geofence" if distance <= radius_meters else "outside_geofence"

    if geofence_status == "outside_geofence":
        raise HTTPException(
            status_code=400,
            detail=f"You are too far from this space to submit feedback. Distance: {round(distance, 2)} m",
        )

    feedback = Feedback(
        space_id=payload.space_id,
        user_name=payload.user_name,
        issue_type=payload.issue_type,
        message=payload.message,
        latitude=payload.latitude,
        longitude=payload.longitude,
        distance_meters=round(distance, 2),
        geofence_status=geofence_status,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    if _is_maintenance_issue(payload.issue_type, payload.message):
        severity = _maintenance_severity(payload.issue_type, payload.message)

        alert = MaintenanceAlert(
            space_id=payload.space_id,
            title=f"{payload.issue_type} issue reported in {space.name}",
            description=(
                f"User {payload.user_name} reported: {payload.message}. "
                f"Feedback was submitted within geofence and should be reviewed."
            ),
            severity=severity,
            status="Open",
            source="feedback",
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

    return feedback