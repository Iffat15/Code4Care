from agents.triage_agent import run_triage
from services.hospital_service import find_available_bed
from models.booking import Booking

# ---------------------------------------------------------
# Process SOS Request
# ---------------------------------------------------------
# Business Flow:
# 1. Run AI triage on symptoms → determine severity level.
# 2. Find available bed based on severity.
# 3. If no beds available → return failure response.
# 4. Reduce available bed count (temporary reservation).
# 5. Create booking with status = "pending".
# 6. Return booking ID for admin approval workflow.
#
# NOTE:
# - Ambulance is NOT assigned here.
# - Ambulance assignment happens only after admin approval.
# - Bed is reduced immediately to prevent overbooking.
def process_sos(db, patient_name: str, symptoms: str, ambulance_requested: bool):
    #find hospital
    
    # Step 1: Determine severity using triage agent
    # Example output: {"severity": "high"} or {"severity": "medium"}
    triage_result = run_triage(symptoms)
    severity = triage_result["severity"]
    
    #find the available beds in hospital
    # Step 2: Find available bed based on severity
    # High severity → ICU
    # Medium/Low severity → General
    bed = find_available_bed(db, severity)

    # Step 3: If no bed available, stop process
    if not bed:
        return {"message": "No beds available"}

    # Step 4: Reserve bed immediately
    # This prevents race conditions where multiple users book same bed
    bed.available -= 1

    #book a bed in the hospital
    # Step 5: Create booking entry (awaiting admin approval)
    booking = Booking(
        patient_name=patient_name,
        hospital_id=bed.hospital_id,
        severity=severity,
        ambulance_requested=ambulance_requested,
        status="pending"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Step 6: Return confirmation response
    return {
        "message": "Booking created. Awaiting admin approval.",
        "booking_id": booking.id,
        "ambulance_requested": ambulance_requested
    }