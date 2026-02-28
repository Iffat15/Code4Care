from models.booking import Booking
from models.bed import Bed
from services.ambulance_service import assign_ambulance

def get_booking(db, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return {"message": "Booking not found"}

    return {
        "id": booking.id,
        "patient_name": booking.patient_name,
        "status": booking.status,
        "hospital_id": booking.hospital_id,
        "severity": booking.severity
    }


def approve_booking(db, booking_id: int):

    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return {"message": "Booking not found"}

    booking.status = "approved"

    ambulance_info = None

    if booking.ambulance_requested:
        ambulance = assign_ambulance(db, booking.hospital_id)

        if ambulance:
            ambulance_info = {
                "ambulance_id": ambulance.id,
                "driver_name": ambulance.driver_name
            }
        else:
            ambulance_info = "No ambulance available"

    db.commit()

    return {
        "message": "Booking approved",
        "ambulance_assignment": ambulance_info
    }

def reject_booking(db, booking_id: int):

    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return {"message": "Booking not found"}

    # Restore bed count if rejected
    bed_type = "ICU" if booking.severity == "high" else "General"

    bed = db.query(Bed).filter(
        Bed.hospital_id == booking.hospital_id,
        Bed.bed_type == bed_type
    ).first()

    if bed:
        bed.available += 1

    booking.status = "rejected"

    db.commit()

    return {"message": "Booking rejected and bed restored"}

