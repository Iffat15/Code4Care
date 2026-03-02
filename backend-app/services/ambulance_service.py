# from models.ambulance import Ambulance

# # ---------------------------------------------------------
# # Assign Ambulance to a Booking
# # ---------------------------------------------------------
# # Business Logic:
# # 1. Find first available ambulance for the given hospital.
# # 2. If none available → return None.
# # 3. If available → mark ambulance as unavailable.
# # 4. Commit change immediately to prevent double assignment.
# #
# # Used during:
# # - Booking approval process
# #
# # Returns:
# # - Ambulance object if successfully assigned
# # - None if no ambulance available
# def assign_ambulance(db, hospital_id: int):

#     # Step 1: Find available ambulance in the same hospital
#     ambulance = db.query(Ambulance).filter(
#         Ambulance.hospital_id == hospital_id,
#         Ambulance.available == True
#     ).first()

#     # Step 2: If no ambulance available, return None
#     if not ambulance:
#         return None

#     # Step 3: Mark ambulance as unavailable (reserved)
#     # This prevents multiple bookings from using same ambulance
#     ambulance.available = False
    
#     # Step 4: Save change immediately
#     db.commit()

#     return ambulance


# services/ambulance_service.py

from sqlalchemy.orm import Session
from models.ambulance import Ambulance


# ==========================================================
# FETCH AVAILABLE AMBULANCES (FOR ORCHESTRATION)
# ==========================================================
def get_available_ambulances(db: Session):
    """
    Returns all available ambulances
    (Hospital + NGO).

    No mutation happens here.
    """

    ambulances = db.query(Ambulance).filter(
        Ambulance.available == True
    ).all()

    ambulance_options = []

    for amb in ambulances:
        ambulance_options.append({
            "ambulance_id": amb.id,
            "provider_type": amb.provider_type,  # "hospital" / "ngo"
            "support_type": amb.support_type,    # "ALS" / "BLS"
            "hospital_id": amb.hospital_id,
            "available": amb.available
        })

    return ambulance_options


# ==========================================================
# RESERVE AMBULANCE (ATOMIC SAFE LOCK)
# ==========================================================
def reserve_ambulance(
    db: Session,
    ambulance_id: int
):
    """
    Atomically reserves an ambulance.

    Uses row-level locking to prevent double booking.

    Returns:
        Ambulance object if successful
        None if not available
    """

    ambulance = db.query(Ambulance).filter(
        Ambulance.id == ambulance_id,
        Ambulance.available == True
    ).with_for_update().first()

    if not ambulance:
        return None

    ambulance.available = False

    # DO NOT COMMIT HERE
    # Let calling service handle transaction

    return ambulance


# ==========================================================
# RELEASE AMBULANCE
# ==========================================================
def release_ambulance(
    db: Session,
    ambulance_id: int
):
    """
    Releases ambulance back into pool.
    Used after booking completion or cancellation.
    """

    ambulance = db.query(Ambulance).filter(
        Ambulance.id == ambulance_id
    ).with_for_update().first()

    if not ambulance:
        return None

    ambulance.available = True
    return ambulance


# ==========================================================
# UPDATE AMBULANCE STATUS
# ==========================================================
def update_ambulance_status(
    db: Session,
    ambulance_id: int,
    status: str
):
    """
    Updates ambulance operational status.

    Example statuses:
        - available
        - dispatched
        - en_route
        - at_scene
        - completed
        - maintenance
    """

    ambulance = db.query(Ambulance).filter(
        Ambulance.id == ambulance_id
    ).with_for_update().first()

    if not ambulance:
        return None

    ambulance.status = status
    return ambulance