from statistics import mean, pstdev

from sqlalchemy.orm import Session

from app.models.space import Space
from app.services.analytics_service import get_space_utilization_summary

IDEAL_UTILIZATION = 65.0
IDLE_THRESHOLD = 20.0
OVERUTILIZED_THRESHOLD = 80.0


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _status(avg_util: float) -> str:
    if avg_util < IDLE_THRESHOLD:
        return "Idle"
    if avg_util > OVERUTILIZED_THRESHOLD:
        return "Overutilized"
    return "Normal"


def _fit_score(avg_util: float) -> float:
    """
    How close a space is to the ideal utilization target.
    65% is treated as healthy/efficient utilization.
    """
    deviation = abs(avg_util - IDEAL_UTILIZATION)
    return _clamp(100.0 - (deviation * 2.3))


def _balance_score(space_avgs: list[float]) -> float:
    if not space_avgs:
        return 0.0

    fit_scores = [_fit_score(avg) for avg in space_avgs]
    average_fit = mean(fit_scores)

    spread = pstdev(space_avgs) if len(space_avgs) > 1 else 0.0

    # Normalize spread into 0–100 scale
    spread_score = _clamp(100 - (spread * 1.2))

    # Combine both instead of subtracting (important)
    final_score = (average_fit * 0.6) + (spread_score * 0.4)

    return round(_clamp(final_score), 2)

def _pair_score(over_space: dict, under_space: dict) -> float:
    util_gap = over_space["average_utilization"] - under_space["average_utilization"]
    if util_gap <= 0:
        return 0.0

    # NEW: enforce same type (or compatible)
    if over_space["space_type"] != under_space["space_type"]:
        return 0.0  # completely reject invalid pairing

    bigger_capacity = max(over_space["capacity"], under_space["capacity"])
    smaller_capacity = min(over_space["capacity"], under_space["capacity"])
    capacity_fit = (smaller_capacity / bigger_capacity) * 100 if bigger_capacity else 0

    building_bonus = 8.0 if over_space["building"] == under_space["building"] else 0.0

    score = (util_gap * 0.8) + (capacity_fit * 0.25) + building_bonus
    return round(_clamp(score), 2)

def _simulate_move(current_values: dict[int, float], from_id: int, to_id: int, transfer: float):
    simulated = current_values.copy()
    simulated[from_id] = _clamp(simulated[from_id] - transfer)
    simulated[to_id] = _clamp(simulated[to_id] + transfer)
    return simulated


def get_optimization_recommendations(db: Session, days: int = 30):
    spaces = db.query(Space).order_by(Space.name.asc()).all()

    analyzed_spaces = []
    for space in spaces:
        summary = get_space_utilization_summary(db, space.id, days)
        avg_util = summary["summary"]["average_utilization"]

        analyzed_spaces.append(
            {
                "id": space.id,
                "name": space.name,
                "building": space.building,
                "capacity": space.capacity,
                "space_type": space.space_type,
                "average_utilization": avg_util,
                "status": _status(avg_util),
                "fit_score": _fit_score(avg_util),
            }
        )

    if not analyzed_spaces:
        return {
            "analysis_window_days": days,
            "summary": {
                "total_spaces": 0,
                "idle_spaces": 0,
                "normal_spaces": 0,
                "overutilized_spaces": 0,
                "current_average_utilization": 0,
                "current_balance_score": 0,
                "proposed_balance_score": 0,
                "improvement_percentage": 0,
            },
            "recommendations": [],
            "spaces": [],
        }

    avg_values = [s["average_utilization"] for s in analyzed_spaces]
    current_balance_score = _balance_score(avg_values)
    current_average_utilization = round(mean(avg_values), 2)

    idle_spaces = [s for s in analyzed_spaces if s["status"] == "Idle"]
    normal_spaces = [s for s in analyzed_spaces if s["status"] == "Normal"]
    overutilized_spaces = [s for s in analyzed_spaces if s["status"] == "Overutilized"]

    recommendations = []
    simulated_values = {s["id"]: s["average_utilization"] for s in analyzed_spaces}
    used_targets = set()

    # First: fix strong imbalance by pairing overutilized with idle/underused rooms
    for over_space in sorted(overutilized_spaces, key=lambda x: x["average_utilization"], reverse=True):
        best_candidate = None
        best_score = 0.0

        for candidate in sorted(idle_spaces + normal_spaces, key=lambda x: x["average_utilization"]):
            if candidate["id"] == over_space["id"] or candidate["id"] in used_targets:
                continue

            candidate_score = _pair_score(over_space, candidate)

            if candidate_score > best_score:
                best_score = candidate_score
                best_candidate = candidate

        if best_candidate and best_score >= 20:
            # Move enough load to make a visible difference, but not too much.
            util_gap = over_space["average_utilization"] - best_candidate["average_utilization"]
            transfer = round(min(max(util_gap * 0.35, 5.0), 18.0), 2)

            # simulate the move for proposed score
            simulated_values = _simulate_move(
                simulated_values,
                over_space["id"],
                best_candidate["id"],
                transfer,
            )

            recommendations.append(
                {
                    "type": "Move class allocation",
                    "from_space": {
                        "id": over_space["id"],
                        "name": over_space["name"],
                        "building": over_space["building"],
                        "capacity": over_space["capacity"],
                        "average_utilization": over_space["average_utilization"],
                    },
                    "to_space": {
                        "id": best_candidate["id"],
                        "name": best_candidate["name"],
                        "building": best_candidate["building"],
                        "capacity": best_candidate["capacity"],
                        "average_utilization": best_candidate["average_utilization"],
                    },
                    "reason": (
                        f"{over_space['name']} is crowded while {best_candidate['name']} has spare capacity."
                    ),
                    "transfer_points": transfer,
                    "estimated_improvement": round(best_score / 2, 2),
                    "confidence": "High" if best_score >= 50 else "Medium",
                }
            )
            used_targets.add(best_candidate["id"])

    # Second: if no strong imbalance exists, still give AI-like fine tuning suggestions
    if not recommendations:
        for space in sorted(analyzed_spaces, key=lambda x: abs(x["average_utilization"] - IDEAL_UTILIZATION), reverse=True):
            deviation = abs(space["average_utilization"] - IDEAL_UTILIZATION)

            if deviation < 8:
                continue

            if space["status"] == "Idle":
                action = "Reduce the number of scheduled sessions or merge this room with nearby allocations."
                impact = round(min(15.0, deviation * 0.9), 2)
            elif space["status"] == "Overutilized":
                action = "Shift one or more classes to a better-fit room with higher spare capacity."
                impact = round(min(20.0, deviation * 1.1), 2)
            else:
                action = "Fine-tune timetable placement to better match capacity and demand."
                impact = round(min(10.0, deviation * 0.6), 2)

            recommendations.append(
                {
                    "type": "AI-assisted fine tuning",
                    "from_space": {
                        "id": space["id"],
                        "name": space["name"],
                        "building": space["building"],
                        "capacity": space["capacity"],
                        "average_utilization": space["average_utilization"],
                    },
                    "to_space": None,
                    "reason": action,
                    "transfer_points": 0,
                    "estimated_improvement": impact,
                    "confidence": "Medium",
                }
            )

    proposed_balance_score = _balance_score(list(simulated_values.values()))
    improvement_percentage = round(proposed_balance_score - current_balance_score, 2)

    return {
        "analysis_window_days": days,
        "summary": {
            "total_spaces": len(analyzed_spaces),
            "idle_spaces": len(idle_spaces),
            "normal_spaces": len(normal_spaces),
            "overutilized_spaces": len(overutilized_spaces),
            "current_average_utilization": current_average_utilization,
            "current_balance_score": current_balance_score,
            "proposed_balance_score": proposed_balance_score,
            "improvement_percentage": improvement_percentage,
        },
        "recommendations": recommendations,
        "spaces": analyzed_spaces,
    }