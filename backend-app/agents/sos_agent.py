# agents/sos_agent.py

from typing import Dict
from datetime import datetime


def run_sos_agent(symptoms: str, ambulance_requested: bool) -> Dict:
    """
    SOS Agent:
    Determines urgency level and context completeness.

    This agent DOES NOT:
    - Book beds
    - Assign hospitals
    - Modify DB

    It only interprets the emergency request.
    """

    symptoms_lower = symptoms.lower()

    # Basic risk keyword detection
    high_risk_keywords = [
        "unconscious",
        "not breathing",
        "chest pain",
        "severe bleeding",
        "accident",
        "stroke",
        "heart attack"
    ]

    urgency = "normal"

    for keyword in high_risk_keywords:
        if keyword in symptoms_lower:
            urgency = "very_serious"
            break

    if urgency != "very_serious" and len(symptoms) > 100:
        urgency = "serious"

    reasoning = f"""
    SOS Agent Analysis:
    - Symptoms length: {len(symptoms)}
    - High-risk keyword detected: {urgency == 'very_serious'}
    - Ambulance requested: {ambulance_requested}
    """

    return {
        "urgency": urgency,
        "needs_ambulance": ambulance_requested or urgency == "very_serious",
        "data_completeness": "partial" if len(symptoms) < 20 else "sufficient",
        "timestamp": datetime.utcnow().isoformat(),
        "reasoning": reasoning.strip()
    }