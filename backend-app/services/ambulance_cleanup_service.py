from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.booking import Booking
from models.ambulance import Ambulance

# Now we implement real backend engineering 

# If:

# Ambulance assigned

# Patient never admitted

# After X minutes → release automatically

# We’ll simulate timeout-based release.

# ---------------------------------------------------------
# Auto Release Ambulances (Timeout Mechanism)
# ---------------------------------------------------------
# Business Problem:
# If an ambulance is assigned but the patient is never admitted,
# the ambulance should not remain locked forever.
#
# Solution:
# 1. Find all bookings that are:
#    - status = "approved"
#    - have an approved_at timestamp
# 2. Check if approval time exceeded configured timeout.
# 3. If expired:
#       - Release assigned ambulance (if any)
#       - Mark booking as "cancelled"
# 4. Commit all changes.
#
# This function should be triggered by:
# - A background scheduler (e.g., Celery, APScheduler, cron job)
# - Running every few minutes
#
# Important:
# - Prevents ambulance resource leakage
# - Ensures fair resource redistribution
# - Keeps system self-healing
#
def auto_release_ambulances(db: Session):

    # Configurable timeout window (in minutes)
    # After this time, unadmitted bookings are cancelled
    timeout_minutes = 10   # configurable

    # Step 1: Fetch all approved bookings
    # These are bookings where:
    # - Admin has approved
    # - Ambulance may have been assigned
    expired_bookings = db.query(Booking).filter(
        Booking.status == "approved",
        Booking.approved_at != None
    ).all()

    # Step 2: Iterate through each approved booking
    for booking in expired_bookings:

        # Calculate time passed since approval
        time_passed = datetime.utcnow() - booking.approved_at

        # Step 3: Check if timeout exceeded
        if time_passed > timedelta(minutes=timeout_minutes):

            # If ambulance was assigned → release it
            if booking.ambulance_id:
                ambulance = db.query(Ambulance).filter(
                    Ambulance.id == booking.ambulance_id
                ).first()

                if ambulance:
                    # Mark ambulance available again
                    ambulance.available = True
             # Step 4: Cancel booking due to timeout
            booking.status = "cancelled"
    # Step 5: Commit all updates in one transaction
    db.commit()