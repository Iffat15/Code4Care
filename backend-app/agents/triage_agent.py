# agents/triage_agent.py

from typing import Dict


def run_triage(symptoms: str, context: Dict) -> Dict:
    """
    Triage Agent:
    Determines required bed type, oxygen, specialty, time sensitivity.

    Pure reasoning layer.
    """

    symptoms_lower = symptoms.lower()

    required_bed_type = "General"
    oxygen_required = False
    speciality = "general_medicine"
    time_sensitivity = "medium"
    confidence = 0.75

    if any(word in symptoms_lower for word in ["chest pain", "heart", "stroke"]):
        required_bed_type = "ICU"
        oxygen_required = True
        speciality = "cardiology"
        time_sensitivity = "high"
        confidence = 0.92

    elif any(word in symptoms_lower for word in ["accident", "bleeding", "trauma"]):
        required_bed_type = "ICU"
        speciality = "trauma"
        time_sensitivity = "high"
        confidence = 0.90

    elif "fever" in symptoms_lower:
        required_bed_type = "General"
        speciality = "internal_medicine"
        time_sensitivity = "low"
        confidence = 0.80

    reasoning = f"""
    Triage Decision:
    - Bed Type: {required_bed_type}
    - Oxygen Required: {oxygen_required}
    - Specialty: {speciality}
    - Time Sensitivity: {time_sensitivity}
    - Context Urgency: {context.get('urgency')}
    """

    return {
        "required_bed_type": required_bed_type,
        "oxygen_required": oxygen_required,
        "speciality": speciality,
        "time_sensitivity": time_sensitivity,
        "confidence": confidence,
        "reasoning": reasoning.strip()
    }