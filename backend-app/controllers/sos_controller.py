from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services.sos_service import process_sos

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sos")
def trigger_sos(patient_name: str, symptoms: str, ambulance_requested: bool,db: Session = Depends(get_db)):
    return process_sos(db, patient_name, symptoms, ambulance_requested)