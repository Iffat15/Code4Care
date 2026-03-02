from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.admin_service import approve_booking, reject_booking, get_booking
from models.booking import Booking
from models.ambulance import Ambulance

router = APIRouter(prefix="/admin")

# Dependency to get DB session for each request
# Ensures session is properly closed after request completes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# Fetch booking status
# ---------------------------------------------------------
# Returns the current details and status of a booking
# Used by admin to track lifecycle:
# pending → approved → admitted → completed / cancelled
@router.get("/booking_status/{booking_id}")
def fetch_booking(booking_id: int, db: Session = Depends(get_db)):
    return get_booking(db, booking_id)

# ---------------------------------------------------------
# Approve booking
# ---------------------------------------------------------
# Approves a pending booking.
# Business logic handled in service layer:
# - Changes status to "approved"
# - Assigns ambulance (if requested & available)
# - Reduces bed count
# - Sets approved_at timestamp
@router.post("/approve/{booking_id}")
def approve(booking_id: int, db: Session = Depends(get_db)):
    return approve_booking(db, booking_id)

# ---------------------------------------------------------
# Reject booking
# ---------------------------------------------------------
# Rejects a pending booking.
# Business logic handled in service layer:
# - Changes status to "rejected"
# - No bed or ambulance allocation happens
@router.post("/reject/{booking_id}")
def reject(booking_id: int, db: Session = Depends(get_db)):
    return reject_booking(db, booking_id)

# ---------------------------------------------------------
# Admit patient
# ---------------------------------------------------------
# Moves booking from "approved" → "admitted"
# This simulates patient arrival at hospital.
#
# Logic:
# - Validate booking exists
# - Ensure booking is already approved
# - Update status to "admitted"
# - Release assigned ambulance (mark available=True)
#   because patient has reached hospital
@router.put("/admit/{booking_id}")
def admit_patient(booking_id: int, db: Session = Depends(get_db)):

    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status != "approved":
        raise HTTPException(status_code=400, detail="Only approved bookings can be admitted")

    # ✅ Mark as admitted
    booking.status = "admitted"

    # ✅ Release ambulance if assigned
    if booking.ambulance_id:
        ambulance = db.query(Ambulance).filter(
            Ambulance.id == booking.ambulance_id
        ).first()

        if ambulance:
            ambulance.available = True

    db.commit()

    return {
        "message": "Patient admitted successfully",
        "booking_id": booking.id
    }

# ---------------------------------------------------------
# Complete booking
# ---------------------------------------------------------
# Moves booking from "admitted" → "completed"
# This simulates patient discharge / case closure.
#
# Logic:
# - Ensure booking exists
# - Ensure patient is admitted
# - Update status to "completed"
# - Final lifecycle state (no further transitions)
# pending → approved → admitted → completed
@router.put("/complete/{booking_id}")
def complete_booking(booking_id: int, db: Session = Depends(get_db)):

    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status != "admitted":
        raise HTTPException(status_code=400, detail="Only admitted bookings can be completed")

    booking.status = "completed"

    db.commit()

    return {
        "message": "Booking completed successfully",
        "booking_id": booking.id
    }