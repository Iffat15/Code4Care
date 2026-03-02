# from datetime import datetime, timedelta
# from sqlalchemy.orm import Session
# from models.booking import Booking
# from models.ambulance import Ambulance

# # Now we implement real backend engineering 

# # If:

# # Ambulance assigned

# # Patient never admitted

# # After X minutes → release automatically

# # We’ll simulate timeout-based release.

# # ---------------------------------------------------------
# # Auto Release Ambulances (Timeout Mechanism)
# # ---------------------------------------------------------
# # Business Problem:
# # If an ambulance is assigned but the patient is never admitted,
# # the ambulance should not remain locked forever.
# #
# # Solution:
# # 1. Find all bookings that are:
# #    - status = "approved"
# #    - have an approved_at timestamp
# # 2. Check if approval time exceeded configured timeout.
# # 3. If expired:
# #       - Release assigned ambulance (if any)
# #       - Mark booking as "cancelled"
# # 4. Commit all changes.
# #
# # This function should be triggered by:
# # - A background scheduler (e.g., Celery, APScheduler, cron job)
# # - Running every few minutes
# #
# # Important:
# # - Prevents ambulance resource leakage
# # - Ensures fair resource redistribution
# # - Keeps system self-healing
# #
# def auto_release_ambulances(db: Session):

#     # Configurable timeout window (in minutes)
#     # After this time, unadmitted bookings are cancelled
#     timeout_minutes = 10   # configurable

#     # Step 1: Fetch all approved bookings
#     # These are bookings where:
#     # - Admin has approved
#     # - Ambulance may have been assigned
#     expired_bookings = db.query(Booking).filter(
#         Booking.status == "approved",
#         Booking.approved_at != None
#     ).all()

#     # Step 2: Iterate through each approved booking
#     for booking in expired_bookings:

#         # Calculate time passed since approval
#         time_passed = datetime.utcnow() - booking.approved_at

#         # Step 3: Check if timeout exceeded
#         if time_passed > timedelta(minutes=timeout_minutes):

#             # If ambulance was assigned → release it
#             if booking.ambulance_id:
#                 ambulance = db.query(Ambulance).filter(
#                     Ambulance.id == booking.ambulance_id
#                 ).first()

#                 if ambulance:
#                     # Mark ambulance available again
#                     ambulance.available = True
#              # Step 4: Cancel booking due to timeout
#             booking.status = "cancelled"
#     # Step 5: Commit all updates in one transaction
#     db.commit()


# services/ambulance_cleanup_service.py

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.booking import Booking

from services.ambulance_service import release_ambulance
from services.hospital_service import release_bed


# ==========================================================
# AUTO RELEASE AMBULANCES (TIMEOUT CLEANUP)
# ==========================================================
def auto_release_ambulances(db: Session):
    """
    Automatically cancels bookings that exceeded timeout window.

    For each expired booking:
        - Release ambulance (if any)
        - Release bed
        - Mark booking as cancelled
        - Store cancellation metadata
    """

    timeout_minutes = 10  # configurable

    now = datetime.utcnow()

    # Fetch approved bookings only
    approved_bookings = db.query(Booking).filter(
        Booking.status == "approved",
        Booking.approved_at != None
    ).all()

    for booking in approved_bookings:

        time_passed = now - booking.approved_at

        if time_passed > timedelta(minutes=timeout_minutes):

            # Lock booking row to prevent race conditions
            locked_booking = db.query(Booking).filter(
                Booking.id == booking.id
            ).with_for_update().first()

            if not locked_booking:
                continue

            # Double-check status after lock
            if locked_booking.status != "approved":
                continue

            # --------------------------------------------------
            # RELEASE AMBULANCE
            # --------------------------------------------------
            if locked_booking.ambulance_id:
                release_ambulance(
                    db,
                    locked_booking.ambulance_id
                )

            # --------------------------------------------------
            # RELEASE BED
            # --------------------------------------------------
            release_bed(
                db,
                hospital_id=locked_booking.hospital_id,
                bed_type=locked_booking.triage_level
            )

            # --------------------------------------------------
            # UPDATE BOOKING STATUS
            # --------------------------------------------------
            locked_booking.status = "cancelled"
            locked_booking.cancelled_at = now
            locked_booking.cancellation_reason = "timeout_auto_release"

    # Commit once after all updates
    db.commit()