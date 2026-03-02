from models.booking import Booking
from models.bed import Bed
from services.ambulance_service import assign_ambulance
from services.ambulance_cleanup_service import auto_release_ambulances
from datetime import datetime


# ---------------------------------------------------------
# Get Booking Details
# ---------------------------------------------------------
# Fetches booking information by ID.
# Used by admin to check lifecycle state and details.
# Returns minimal booking data (can be expanded later).
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

# ---------------------------------------------------------
# Approve Booking
# ---------------------------------------------------------
# Business Logic:
# 1. Run auto-cleanup to release expired ambulances.
# 2. Validate booking exists.
# 3. Update status → "approved".
# 4. Store approval timestamp (for timeout tracking).
# 5. If ambulance requested:
#       - Try assigning available ambulance.
#       - Return assignment details.
#
# NOTE:
# Bed reduction should already happen at booking creation.
def approve_booking(db, booking_id: int):
    auto_release_ambulances(db)
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return {"message": "Booking not found"}

    booking.status = "approved"
    booking.approved_at = datetime.utcnow()

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

# ---------------------------------------------------------
# Reject Booking
# ---------------------------------------------------------
# Business Logic:
# 1. Validate booking exists.
# 2. Restore previously reserved bed count.
# 3. Update status → "rejected".
#
# Reason:
# When booking was created, bed availability was reduced.
# If rejected, we must restore capacity.
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

