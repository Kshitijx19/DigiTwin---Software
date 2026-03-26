from datetime import datetime
from sqlalchemy.orm import Session

from app.models.maintenance import MaintenanceAlert
from app.models.space import Space
from app.services.analytics_service import get_space_utilization_summary


def generate_maintenance_alerts(db: Session, days: int = 30):
    """
    Generates alerts for spaces that are repeatedly overutilized.
    """
    spaces = db.query(Space).all()
    created = 0

    for space in spaces:
        summary = get_space_utilization_summary(db, space.id, days)
        over_count = summary["summary"]["overutilized_records"]
        avg_util = summary["summary"]["average_utilization"]

        existing_open = (
            db.query(MaintenanceAlert)
            .filter(
                MaintenanceAlert.space_id == space.id,
                MaintenanceAlert.status == "Open",
                MaintenanceAlert.source == "utilization",
            )
            .first()
        )

        if avg_util > 85 or over_count >= 10:
            if not existing_open:
                alert = MaintenanceAlert(
                    space_id=space.id,
                    title=f"High usage warning for {space.name}",
                    description=(
                        f"{space.name} has average utilization of {avg_util}% "
                        f"with {over_count} overutilized records in the last {days} days."
                    ),
                    severity="High" if avg_util <= 95 else "Critical",
                    status="Open",
                    source="utilization",
                )
                db.add(alert)
                created += 1

    db.commit()

    return {
        "message": "Maintenance scan completed",
        "alerts_created": created,
    }


def get_all_maintenance_alerts(db: Session):
    return (
        db.query(MaintenanceAlert)
        .order_by(MaintenanceAlert.created_at.desc())
        .all()
    )