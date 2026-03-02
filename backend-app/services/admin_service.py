# from models.booking import Booking
# from models.bed import Bed
# from services.ambulance_service import assign_ambulance
# from services.ambulance_cleanup_service import auto_release_ambulances
# from datetime import datetime


# # ---------------------------------------------------------
# # Get Booking Details
# # ---------------------------------------------------------
# # Fetches booking information by ID.
# # Used by admin to check lifecycle state and details.
# # Returns minimal booking data (can be expanded later).
# def get_booking(db, booking_id: int):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()

#     if not booking:
#         return {"message": "Booking not found"}

#     return {
#         "id": booking.id,
#         "patient_name": booking.patient_name,
#         "status": booking.status,
#         "hospital_id": booking.hospital_id,
#         "severity": booking.severity
#     }

# # ---------------------------------------------------------
# # Approve Booking
# # ---------------------------------------------------------
# # Business Logic:
# # 1. Run auto-cleanup to release expired ambulances.
# # 2. Validate booking exists.
# # 3. Update status → "approved".
# # 4. Store approval timestamp (for timeout tracking).
# # 5. If ambulance requested:
# #       - Try assigning available ambulance.
# #       - Return assignment details.
# #
# # NOTE:
# # Bed reduction should already happen at booking creation.
# def approve_booking(db, booking_id: int):
#     auto_release_ambulances(db)
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()

#     if not booking:
#         return {"message": "Booking not found"}

#     booking.status = "approved"
#     booking.approved_at = datetime.utcnow()

#     ambulance_info = None

#     if booking.ambulance_requested:
#         ambulance = assign_ambulance(db, booking.hospital_id)

#         if ambulance:
#             ambulance_info = {
#                 "ambulance_id": ambulance.id,
#                 "driver_name": ambulance.driver_name
#             }
#         else:
#             ambulance_info = "No ambulance available"

#     db.commit()

#     return {
#         "message": "Booking approved",
#         "ambulance_assignment": ambulance_info
#     }

# # ---------------------------------------------------------
# # Reject Booking
# # ---------------------------------------------------------
# # Business Logic:
# # 1. Validate booking exists.
# # 2. Restore previously reserved bed count.
# # 3. Update status → "rejected".
# #
# # Reason:
# # When booking was created, bed availability was reduced.
# # If rejected, we must restore capacity.
# def reject_booking(db, booking_id: int):

#     booking = db.query(Booking).filter(Booking.id == booking_id).first()

#     if not booking:
#         return {"message": "Booking not found"}

#     # Restore bed count if rejected
#     bed_type = "ICU" if booking.severity == "high" else "General"

#     bed = db.query(Bed).filter(
#         Bed.hospital_id == booking.hospital_id,
#         Bed.bed_type == bed_type
#     ).first()

#     if bed:
#         bed.available += 1

#     booking.status = "rejected"

#     db.commit()

#     return {"message": "Booking rejected and bed restored"}



# services/admin_service.py

from sqlalchemy.orm import Session
from datetime import datetime

from models.booking import Booking

from services.hospital_service import release_bed
from services.ambulance_service import (
    reserve_ambulance,
    release_ambulance
)
from services.ambulance_cleanup_service import auto_release_ambulances


# ==========================================================
# GET BOOKING DETAILS
# ==========================================================
def get_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        return {"message": "Booking not found"}

    return {
        "id": booking.id,
        "patient_name": booking.patient_name,
        "status": booking.status,
        "hospital_id": booking.hospital_id,
        "triage_level": booking.triage_level,
        "ambulance_id": booking.ambulance_id,
        "severity": booking.severity,
        "confidence_score": booking.confidence_score
    }


# ==========================================================
# APPROVE BOOKING
# ==========================================================
def approve_booking(db: Session, booking_id: int):
    """
    Admin approval:
    - Ensures booking exists
    - Marks approved
    - If ambulance not pre-reserved → reserve now
    - Uses atomic operations
    """

    auto_release_ambulances(db)

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).with_for_update().first()

    if not booking:
        return {"message": "Booking not found"}

    if booking.status != "pending":
        return {"message": f"Booking already {booking.status}"}

    booking.status = "approved"
    booking.approved_at = datetime.utcnow()

    ambulance_info = None

    # If ambulance was requested but not reserved earlier
    if booking.ambulance_requested and not booking.ambulance_id:

        # AI decision stored in audit trail
        ambulance_decision = booking.ai_reasoning.get("ambulance_decision")

        if ambulance_decision and ambulance_decision.get("ambulance_id"):
            ambulance = reserve_ambulance(
                db,
                ambulance_decision["ambulance_id"]
            )

            if ambulance:
                booking.ambulance_id = ambulance.id
                ambulance_info = {
                    "ambulance_id": ambulance.id,
                    "provider_type": ambulance.provider_type
                }
            else:
                ambulance_info = "Ambulance no longer available"
        else:
            ambulance_info = "No ambulance decision available"

    db.commit()

    return {
        "message": "Booking approved",
        "ambulance_assignment": ambulance_info
    }


# ==========================================================
# REJECT BOOKING
# ==========================================================
def reject_booking(db: Session, booking_id: int):
    """
    Admin rejection:
    - Releases reserved bed
    - Releases ambulance if reserved
    - Updates status
    """

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).with_for_update().first()

    if not booking:
        return {"message": "Booking not found"}

    if booking.status != "pending":
        return {"message": f"Cannot reject booking in {booking.status} state"}

    # ------------------------------------------------------
    # RELEASE BED
    # ------------------------------------------------------
    release_bed(
        db,
        hospital_id=booking.hospital_id,
        bed_type=booking.triage_level
    )

    # ------------------------------------------------------
    # RELEASE AMBULANCE (IF RESERVED)
    # ------------------------------------------------------
    if booking.ambulance_id:
        release_ambulance(
            db,
            booking.ambulance_id
        )

    booking.status = "rejected"
    booking.rejected_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Booking rejected",
        "resources_released": True
    }