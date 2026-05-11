"""
farmscore.py
Core scoring logic for the Farm Score Project.
"""


WEIGHTS = {
    "soil_health": 0.30,
    "water_efficiency": 0.25,
    "biodiversity": 0.20,
    "practices": 0.25,
}

MAX_INPUT = 10  # All input scores are expected on a 0–10 scale


def calculate_score(data: dict) -> dict:
    """
    Calculate a farm's overall score from input metrics.

    Expected keys in `data`:
        - soil_health (0–10)
        - water_usage_efficiency (0–10)
        - biodiversity_score (0–10)
        - irrigation_type (str): 'drip' | 'sprinkler' | 'flood' | 'rainfed'
        - crop_type (str): any string (used for practice bonus)

    Returns a dict with total_score, grade, breakdown, and recommendations.
    """
    soil = _clamp(data.get("soil_health", 0))
    water = _clamp(data.get("water_usage_efficiency", 0))
    biodiversity = _clamp(data.get("biodiversity_score", 0))
    practices = _practices_score(data)

    breakdown = {
        "soil_health": round(soil * WEIGHTS["soil_health"] * 10, 2),
        "water_efficiency": round(water * WEIGHTS["water_efficiency"] * 10, 2),
        "biodiversity": round(biodiversity * WEIGHTS["biodiversity"] * 10, 2),
        "practices": round(practices * WEIGHTS["practices"] * 10, 2),
    }

    total = round(sum(breakdown.values()), 2)
    grade = _grade(total)
    recommendations = _recommendations(data, breakdown)

    return {
        "farm_name": data.get("farm_name", "Unknown Farm"),
        "total_score": total,
        "grade": grade,
        "breakdown": breakdown,
        "recommendations": recommendations,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _clamp(value, lo: float = 0, hi: float = MAX_INPUT) -> float:
    """Clamp a value to [lo, hi]."""
    try:
        return max(lo, min(float(value), hi))
    except (TypeError, ValueError):
        return lo


def _practices_score(data: dict) -> float:
    """
    Derive a 0–10 practices score from irrigation type and crop signals.
    Extend this function to add more sophisticated logic.
    """
    score = 5.0  # baseline

    irrigation_bonuses = {
        "drip": 3.0,
        "sprinkler": 1.5,
        "rainfed": 2.0,
        "flood": -1.0,
    }
    irrigation = str(data.get("irrigation_type", "")).lower().strip()
    score += irrigation_bonuses.get(irrigation, 0)

    # Simple crop-diversity proxy: longer / more descriptive crop type → slight bonus
    crop = str(data.get("crop_type", ""))
    if len(crop) > 5:
        score += 0.5

    return _clamp(score)


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _recommendations(data: dict, breakdown: dict) -> list:
    recs = []

    if breakdown["soil_health"] < 20:
        recs.append("Consider cover cropping or composting to improve soil health.")

    if breakdown["water_efficiency"] < 15:
        recs.append("Switching to drip irrigation can significantly improve water efficiency.")

    if breakdown["biodiversity"] < 12:
        recs.append("Introduce hedgerows or wildflower strips to boost on-farm biodiversity.")

    if breakdown["practices"] < 15:
        irrigation = str(data.get("irrigation_type", "")).lower()
        if irrigation == "flood":
            recs.append("Flood irrigation is water-intensive; consider drip or sprinkler systems.")

    if not recs:
        recs.append("Great work! Keep maintaining your current sustainable farming practices.")

    return recs
