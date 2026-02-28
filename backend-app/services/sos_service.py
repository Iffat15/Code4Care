from agents.triage_agent import run_triage
from services.hospital_service import find_available_bed
from models.booking import Booking
def process_sos(db, patient_name: str, symptoms: str, ambulance_requested: bool):
    #find hospital
    triage_result = run_triage(symptoms)
    severity = triage_result["severity"]
    
    #find the available beds in hospital
    bed = find_available_bed(db, severity)

    if not bed:
        return {"message": "No beds available"}

    bed.available -= 1

    #book a bed in the hospital
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

    return {
        "message": "Booking created. Awaiting admin approval.",
        "booking_id": booking.id,
        "ambulance_requested": ambulance_requested
    }