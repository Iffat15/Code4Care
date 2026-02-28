from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from database import Base

# Now bookings start as pending.
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    severity = Column(String)

    ambulance_requested = Column(Boolean, default=False)
    ambulance_id = Column(Integer, ForeignKey("ambulances.id"), nullable=True)
    status = Column(String, default="pending")
    # pending | approved | rejected