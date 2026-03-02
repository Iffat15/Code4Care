from sqlalchemy import ForeignKey

from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    full_name = Column(String(255), nullable=False)
    age = Column(Integer)
    blood_group = Column(String(10))
    emergency_contact_number = Column(String(20))

    relation = Column(String(50), nullable=True)  # only if not self
    critical_information = Column(String, nullable=True)

    is_self = Column(Boolean, default=True)

    user = relationship("User", back_populates="patients")
    bookings = relationship("Booking", back_populates="patient")