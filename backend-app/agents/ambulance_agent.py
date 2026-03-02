# agents/ambulance_agent.py

from typing import Dict, List


def run_ambulance_agent(triage_decision: Dict, ambulance_options: List[Dict]) -> Dict:
    """
    Ambulance Agent:
    Chooses best ambulance based on:
    - Required support level
    - Distance
    - Availability
    - Type (NGO / Hospital)
    """

    required_support = "ALS" if triage_decision["required_bed_type"] == "ICU" else "BLS"

    filtered = [
        a for a in ambulance_options
        if a["support_type"] == required_support and a["available"]
    ]

    if not filtered:
        return {
            "ambulance_id": None,
            "reasoning": "No suitable ambulance available",
            "confidence": 0.0
        }

    # Prefer closest ambulance
    best = min(filtered, key=lambda x: x["distance_km"])

    reasoning = f"""
    Ambulance Selection:
    - Selected Ambulance: {best['ambulance_id']}
    - Type: {best['provider_type']}
    - Support Level: {best['support_type']}
    - Distance: {best['distance_km']} km
    """

    return {
        "ambulance_id": best["ambulance_id"],
        "provider_type": best["provider_type"],
        "support_type": best["support_type"],
        "confidence": 0.9,
        "reasoning": reasoning.strip()
    }