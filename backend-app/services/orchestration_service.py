# services/orchestration_service.py

from typing import Dict, List

from agents.sos_agent import run_sos_agent
from agents.triage_agent import run_triage
from agents.orchestrator_agent import run_orchestration
from agents.ambulance_agent import run_ambulance_agent


# ==========================================================
# FULL EMERGENCY ORCHESTRATION PIPELINE
# ==========================================================
def run_full_orchestration(
    symptoms: str,
    ambulance_requested: bool,
    hospital_options: List[Dict],
    ambulance_options: List[Dict]
) -> Dict:
    """
    Master AI Orchestration Layer

    This function:
    - Chains all agents
    - Aggregates reasoning
    - Returns final structured decision
    - Does NOT mutate DB

    Steps:
        1. SOS Agent
        2. Triage Agent
        3. Hospital Orchestrator Agent
        4. Ambulance Agent (conditional)
    """

    # ======================================================
    # 1️⃣ SOS AGENT
    # ======================================================
    sos_context = run_sos_agent(
        symptoms=symptoms,
        ambulance_requested=ambulance_requested
    )

    # ======================================================
    # 2️⃣ TRIAGE AGENT
    # ======================================================
    triage_decision = run_triage(
        symptoms=symptoms,
        context=sos_context
    )

    # ======================================================
    # 3️⃣ HOSPITAL ORCHESTRATOR
    # ======================================================
    hospital_decision = run_orchestration(
        triage_decision=triage_decision,
        hospital_options=hospital_options
    )

    # ======================================================
    # 4️⃣ AMBULANCE AGENT (ONLY IF NEEDED)
    # ======================================================
    ambulance_decision = None

    if sos_context["needs_ambulance"] and hospital_decision["hospital_id"]:
        ambulance_decision = run_ambulance_agent(
            triage_decision=triage_decision,
            ambulance_options=ambulance_options
        )

    # ======================================================
    # FINAL DECISION PACKAGE
    # ======================================================
    return {
        "sos_context": sos_context,
        "triage_decision": triage_decision,
        "hospital_decision": hospital_decision,
        "ambulance_decision": ambulance_decision,
        "final_confidence": _calculate_final_confidence(
            triage_decision,
            hospital_decision,
            ambulance_decision
        )
    }


# ==========================================================
# CONFIDENCE AGGREGATION LOGIC
# ==========================================================
def _calculate_final_confidence(
    triage_decision: Dict,
    hospital_decision: Dict,
    ambulance_decision: Dict
) -> float:
    """
    Weighted confidence score.
    """

    scores = []

    if triage_decision:
        scores.append(triage_decision.get("confidence", 0))

    if hospital_decision:
        scores.append(hospital_decision.get("confidence", 0))

    if ambulance_decision:
        scores.append(ambulance_decision.get("confidence", 0))

    if not scores:
        return 0.0

    return round(sum(scores) / len(scores), 2)