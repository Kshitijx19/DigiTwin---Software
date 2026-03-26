# Import necessary modules
from collections import defaultdict  # Used for grouping values (daily, slot-wise)
from datetime import date, timedelta  # Used for date calculations
import random  # Used to generate synthetic data

from sqlalchemy.orm import Session  # DB session handling

# Import database models
from app.models.space import Space
from app.models.utilization import Utilization

# Import schema for returning formatted response
from app.schemas.space import SpaceRead


# ---------------------------------------------------------
#  FUNCTION: Determine utilization status
# ---------------------------------------------------------
def _utilization_status(percent: float) -> str:
    """
    Categorizes utilization into:
    - Idle (<20%)
    - Normal (20–80%)
    - Overutilized (>80%)
    """
    if percent < 20:
        return "Idle"
    if percent > 80:
        return "Overutilized"
    return "Normal"


# ---------------------------------------------------------
#  FUNCTION: Safe random generator
# ---------------------------------------------------------
def _safe_rand(low: int, high: int) -> int:
    """
    Ensures random range is always valid.
    Prevents errors like randint(10, 5)
    """
    low = max(0, low)
    high = max(low, high)
    return random.randint(low, high)


# ---------------------------------------------------------
#  FUNCTION: Generate synthetic utilization data
# ---------------------------------------------------------
def generate_demo_utilization_records(db, space_id: int, days: int = 30):
    """
    Generates fake (simulated) utilization data
    for a given space over a number of days.
    """

    # Fetch space from DB
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise ValueError("Space not found")

    # Ensure valid capacity
    if space.capacity <= 0:
        raise ValueError("Space capacity must be greater than 0")

    # -----------------------------------------------------
    # Assign "personality" to space
    # This ensures different spaces behave differently
    # -----------------------------------------------------
    if space_id % 3 == 0:
        mode = "idle"  # low usage
    elif space_id % 3 == 1:
        mode = "overutilized"  # high usage
    else:
        mode = "normal"  # moderate usage

    # Define time slots for each day
    slots = ["09:00-11:00", "11:00-13:00", "14:00-16:00"]

    created = 0  # counter
    start_day = date.today() - timedelta(days=days - 1)

    # -----------------------------------------------------
    # Loop through days and slots to generate data
    # -----------------------------------------------------
    for day_offset in range(days):
        record_date = start_day + timedelta(days=day_offset)

        for slot in slots:

            # -------------------------------
            # Generate ACTUAL USERS
            # based on mode
            # -------------------------------
            if mode == "idle":
                # Very low usage
                actual_users = random.randint(0, int(space.capacity * 0.2))

            elif mode == "overutilized":
                # Very high usage (even exceeds capacity)
                actual_users = random.randint(
                    int(space.capacity * 0.85),
                    int(space.capacity * 1.2)
                )

            else:  # normal
                # Moderate usage
                actual_users = random.randint(
                    int(space.capacity * 0.4),
                    int(space.capacity * 0.7)
                )

            # -------------------------------
            # Scheduled users (planned usage)
            # -------------------------------
            scheduled_users = random.randint(
                int(space.capacity * 0.6),
                int(space.capacity * 1.0)
            )

            # Create DB record
            record = Utilization(
                space_id=space_id,
                record_date=record_date,
                time_slot=slot,
                scheduled_users=scheduled_users,
                actual_users=actual_users,
                duration_hours=2,
                source="simulated",
            )

            db.add(record)
            created += 1

    db.commit()

    return {
        "message": f"{mode.upper()} data generated",
        "space_id": space_id,
        "records_created": created,
    }


# ---------------------------------------------------------
#  FUNCTION: Get utilization analytics summary
# ---------------------------------------------------------
def get_space_utilization_summary(db: Session, space_id: int, days: int = 30):
    """
    Computes analytics for a space:
    - average utilization
    - idle/normal/overutilized counts
    - charts data
    """

    # Fetch space
    space = db.query(Space).filter(Space.id == space_id).first()
    if not space:
        raise ValueError("Space not found")

    # Get records for last N days
    cutoff = date.today() - timedelta(days=days - 1)

    records = (
        db.query(Utilization)
        .filter(Utilization.space_id == space_id, Utilization.record_date >= cutoff)
        .order_by(Utilization.record_date.asc(), Utilization.time_slot.asc())
        .all()
    )

    # -----------------------------------------------------
    # If no data → return empty structure
    # -----------------------------------------------------
    if not records:
        return {
            "space": SpaceRead.model_validate(space).model_dump(),
            "summary": {
                "analysis_days": days,
                "total_records": 0,
                "average_utilization": 0,
                "min_utilization": 0,
                "max_utilization": 0,
                "idle_records": 0,
                "normal_records": 0,
                "overutilized_records": 0,
                "idle_hours": 0,
                "peak_time_slot": None,
                "peak_time_slot_utilization": 0,
            },
            "charts": {
                "daily": {"labels": [], "values": []},
                "time_slots": {"labels": [], "values": []},
                "status_counts": {"idle": 0, "normal": 0, "overutilized": 0},
            },
            "recent_records": [],
        }

    # -----------------------------------------------------
    # Initialize structures
    # -----------------------------------------------------
    total_percentages = []
    daily_map = defaultdict(list)
    slot_map = defaultdict(list)
    status_counts = {"idle": 0, "normal": 0, "overutilized": 0}
    total_idle_hours = 0

    # -----------------------------------------------------
    # Process each record
    # -----------------------------------------------------
    for record in records:
        percent = round((record.actual_users / space.capacity) * 100, 2)

        total_percentages.append(percent)

        # Grouping for charts
        daily_map[record.record_date.isoformat()].append(percent)
        slot_map[record.time_slot].append(percent)

        # Determine status
        status = _utilization_status(percent)

        if status == "Idle":
            status_counts["idle"] += 1
            total_idle_hours += record.duration_hours

        elif status == "Overutilized":
            status_counts["overutilized"] += 1

        else:
            status_counts["normal"] += 1

    # -----------------------------------------------------
    # Daily averages
    # -----------------------------------------------------
    daily_labels = sorted(daily_map.keys())
    daily_values = [
        round(sum(values) / len(values), 2)
        for values in (daily_map[label] for label in daily_labels)
    ]

    # -----------------------------------------------------
    # Time slot averages
    # -----------------------------------------------------
    preferred_order = ["09:00-11:00", "11:00-13:00", "14:00-16:00"]

    slot_labels = [slot for slot in preferred_order if slot in slot_map] + [
        slot for slot in slot_map.keys() if slot not in preferred_order
    ]

    slot_values = [
        round(sum(slot_map[slot]) / len(slot_map[slot]), 2)
        for slot in slot_labels
    ]

    # -----------------------------------------------------
    # Peak time slot
    # -----------------------------------------------------
    peak_time_slot = max(
        slot_map.items(),
        key=lambda item: sum(item[1]) / len(item[1]),
    )

    # -----------------------------------------------------
    # Recent records (last 10)
    # -----------------------------------------------------
    recent_records = []
    for record in records[-10:]:
        percent = round((record.actual_users / space.capacity) * 100, 2)

        recent_records.append(
            {
                "date": record.record_date.isoformat(),
                "time_slot": record.time_slot,
                "scheduled_users": record.scheduled_users,
                "actual_users": record.actual_users,
                "utilization_percent": percent,
                "status": _utilization_status(percent),
            }
        )

    # -----------------------------------------------------
    # Final response
    # -----------------------------------------------------
    return {
        "space": SpaceRead.model_validate(space).model_dump(),
        "summary": {
            "analysis_days": days,
            "total_records": len(records),
            "average_utilization": round(sum(total_percentages) / len(total_percentages), 2),
            "min_utilization": min(total_percentages),
            "max_utilization": max(total_percentages),
            "idle_records": status_counts["idle"],
            "normal_records": status_counts["normal"],
            "overutilized_records": status_counts["overutilized"],
            "idle_hours": round(total_idle_hours, 2),
            "peak_time_slot": peak_time_slot[0],
            "peak_time_slot_utilization": round(
                sum(peak_time_slot[1]) / len(peak_time_slot[1]), 2
            ),
        },
        "charts": {
            "daily": {"labels": daily_labels, "values": daily_values},
            "time_slots": {"labels": slot_labels, "values": slot_values},
            "status_counts": status_counts,
        },
        "recent_records": recent_records,
    }