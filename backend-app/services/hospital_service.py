# from sqlalchemy.orm import Session
# from models.hospital import Hospital
# from models.bed import Bed
# from sqlalchemy.orm import Session
# from models.bed import Bed
# # ✔ Hospital Matching Logic
# # High severity → ICU
# # Medium severity → General
# # Checks bed availability


# # ---------------------------------------------------------
# # Find Available Hospital Based on Severity
# # ---------------------------------------------------------
# # Business Logic:
# # - High severity → ICU bed required
# # - Medium/Low severity → General bed required
# # - Checks for any hospital that has at least 1 available bed
# #
# # Returns:
# # - hospital_id if available bed found
# # - None if no hospital has required bed capacity
# #
# # Used during:
# # - Booking creation
# # - SOS processing
# def find_available_hospital(db: Session, severity: str):
#     # Determine required bed type
#     bed_type = "ICU" if severity == "high" else "General"

#     # Query first hospital that has available beds of required type
#     beds = db.query(Bed).filter(
#         Bed.bed_type == bed_type,
#         Bed.available > 0 #atleast 1 bed available
#     ).first()

#     # If bed found, return associated hospital ID
#     if beds:
#         return beds.hospital_id

#     # No hospital has available bed
#     return None

# # ---------------------------------------------------------
# # Find Available Bed Record
# # ---------------------------------------------------------
# # Business Logic:
# # - Determines required bed type from severity
# # - Returns actual Bed object (not just hospital_id)
# #
# # Used when:
# # - Reducing bed count after booking
# # - Allocating bed during approval
# #
# # Returns:
# # - Bed object if available
# # - None if no beds available
# def find_available_bed(db: Session, severity: str):
#     # Determine required bed type
#     bed_type = "ICU" if severity == "high" else "General"

#     # Fetch first available bed record
#     bed = db.query(Bed).filter(
#         Bed.bed_type == bed_type,
#         Bed.available > 0
#     ).first()

#     return bed


# services/hospital_service.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from models.hospital import Hospital
from models.bed import Bed


# ==========================================================
# FETCH HOSPITAL BY ID
# ==========================================================
def get_hospital_by_id(db: Session, hospital_id: int):
    """
    Returns Hospital object or None.
    """
    return db.query(Hospital).filter(
        Hospital.id == hospital_id
    ).first()


# ==========================================================
# GET AVAILABLE BEDS FOR A HOSPITAL
# ==========================================================
def get_available_beds(
    db: Session,
    hospital_id: int,
    bed_type: str
):
    """
    Returns Bed object if available.
    No mutation happens here.
    """
    return db.query(Bed).filter(
        Bed.hospital_id == hospital_id,
        Bed.bed_type == bed_type,
        Bed.available > 0
    ).first()


# ==========================================================
# RESERVE BED (ATOMIC OPERATION)
# ==========================================================
def reserve_bed(
    db: Session,
    hospital_id: int,
    bed_type: str
):
    """
    Atomically reserves a bed.

    Returns:
        Bed object if success
        None if no bed available
    """

    bed = db.query(Bed).filter(
        Bed.hospital_id == hospital_id,
        Bed.bed_type == bed_type,
        Bed.available > 0
    ).with_for_update().first()  # prevents race condition

    if not bed:
        return None

    bed.available -= 1
    return bed


# ==========================================================
# RELEASE BED (ON BOOKING CANCEL / COMPLETION)
# ==========================================================
def release_bed(
    db: Session,
    hospital_id: int,
    bed_type: str
):
    """
    Increases available bed count safely.
    """

    bed = db.query(Bed).filter(
        Bed.hospital_id == hospital_id,
        Bed.bed_type == bed_type
    ).with_for_update().first()

    if not bed:
        return None

    bed.available += 1
    return bed


# ==========================================================
# GET ALL AVAILABLE HOSPITAL OPTIONS (FOR ORCHESTRATION)
# ==========================================================
def get_hospital_options(db: Session):
    """
    Returns structured hospital options
    for orchestration layer.

    This is deterministic data only.
    No scoring logic here.
    """

    beds = db.query(Bed).filter(Bed.available > 0).all()

    hospital_options = []

    for bed in beds:
        hospital_options.append({
            "hospital_id": bed.hospital_id,
            "bed_type": bed.bed_type,
            "available_beds": bed.available
        })

    return hospital_options