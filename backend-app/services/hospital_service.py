from sqlalchemy.orm import Session
from models.hospital import Hospital
from models.bed import Bed
from sqlalchemy.orm import Session
from models.bed import Bed
# ✔ Hospital Matching Logic
# High severity → ICU
# Medium severity → General
# Checks bed availability


# ---------------------------------------------------------
# Find Available Hospital Based on Severity
# ---------------------------------------------------------
# Business Logic:
# - High severity → ICU bed required
# - Medium/Low severity → General bed required
# - Checks for any hospital that has at least 1 available bed
#
# Returns:
# - hospital_id if available bed found
# - None if no hospital has required bed capacity
#
# Used during:
# - Booking creation
# - SOS processing
def find_available_hospital(db: Session, severity: str):
    # Determine required bed type
    bed_type = "ICU" if severity == "high" else "General"

    # Query first hospital that has available beds of required type
    beds = db.query(Bed).filter(
        Bed.bed_type == bed_type,
        Bed.available > 0 #atleast 1 bed available
    ).first()

    # If bed found, return associated hospital ID
    if beds:
        return beds.hospital_id

    # No hospital has available bed
    return None

# ---------------------------------------------------------
# Find Available Bed Record
# ---------------------------------------------------------
# Business Logic:
# - Determines required bed type from severity
# - Returns actual Bed object (not just hospital_id)
#
# Used when:
# - Reducing bed count after booking
# - Allocating bed during approval
#
# Returns:
# - Bed object if available
# - None if no beds available
def find_available_bed(db: Session, severity: str):
    # Determine required bed type
    bed_type = "ICU" if severity == "high" else "General"

    # Fetch first available bed record
    bed = db.query(Bed).filter(
        Bed.bed_type == bed_type,
        Bed.available > 0
    ).first()

    return bed