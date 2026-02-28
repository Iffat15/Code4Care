from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from services.admin_service import approve_booking, reject_booking, get_booking
from models.booking import Booking
from models.ambulance import Ambulance



router = APIRouter(prefix="/admin")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/booking_status/{booking_id}")
def fetch_booking(booking_id: int, db: Session = Depends(get_db)):
    return get_booking(db, booking_id)

@router.post("/approve/{booking_id}")
def approve(booking_id: int, db: Session = Depends(get_db)):
    return approve_booking(db, booking_id)

@router.post("/reject/{booking_id}")
def reject(booking_id: int, db: Session = Depends(get_db)):
    return reject_booking(db, booking_id)



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