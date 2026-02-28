from sqlalchemy.orm import Session
from models.hospital import Hospital
from models.bed import Bed
from sqlalchemy.orm import Session
from models.bed import Bed
# ✔ Hospital Matching Logic

# High severity → ICU

# Medium severity → General

# Checks bed availability

def find_available_hospital(db: Session, severity: str):
    bed_type = "ICU" if severity == "high" else "General"

    beds = db.query(Bed).filter(
        Bed.bed_type == bed_type,
        Bed.available > 0
    ).first()

    if beds:
        return beds.hospital_id

    return None



def find_available_bed(db: Session, severity: str):
    bed_type = "ICU" if severity == "high" else "General"

    bed = db.query(Bed).filter(
        Bed.bed_type == bed_type,
        Bed.available > 0
    ).first()

    return bed