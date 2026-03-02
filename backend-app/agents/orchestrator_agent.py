# agents/orchestrator_agent.py

from typing import Dict, List


def run_orchestration(triage_decision: Dict, hospital_options: List[Dict]) -> Dict:
    """
    Orchestration Agent:
    Selects optimal hospital based on:
    - Required bed type
    - Distance
    - Availability
    - Load

    hospital_options format example:
    [
        {
            "hospital_id": 1,
            "distance_km": 5,
            "available_beds": 3,
            "bed_type": "ICU",
            "load_factor": 0.6
        }
    ]
    """

    required_bed_type = triage_decision["required_bed_type"]

    filtered = [
        h for h in hospital_options
        if h["bed_type"] == required_bed_type and h["available_beds"] > 0
    ]

    if not filtered:
        return {
            "hospital_id": None,
            "reasoning": "No hospitals available for required bed type",
            "confidence": 0.0
        }

    # Scoring logic
    for hospital in filtered:
        score = (
            (1 / (hospital["distance_km"] + 1)) * 0.5 +
            (hospital["available_beds"] * 0.3) -
            (hospital["load_factor"] * 0.2)
        )
        hospital["score"] = score

    best = max(filtered, key=lambda x: x["score"])

    reasoning = f"""
    Orchestration Decision:
    - Selected Hospital: {best['hospital_id']}
    - Distance: {best['distance_km']} km
    - Available Beds: {best['available_beds']}
    - Load Factor: {best['load_factor']}
    - Final Score: {best['score']}
    """

    return {
        "hospital_id": best["hospital_id"],
        "bed_type": required_bed_type,
        "confidence": round(best["score"], 2),
        "reasoning": reasoning.strip()
    }