# ✔ Triage Agent (Mock AI)

# Returns:

# severity

# department

def run_triage(symptoms: str):
    # Temporary mock logic
    if "chest pain" in symptoms.lower():
        return {"severity": "high", "department": "cardiology"}
    return {"severity": "medium", "department": "general"}