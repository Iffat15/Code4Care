from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)

    # ----------------------------
    # Core Info
    # ----------------------------
    name = Column(String(255), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    rating = Column(Float, nullable=True)

    # ----------------------------
    # Relationships
    # ----------------------------
    beds = relationship(
        "BedInventory",          # Must match your actual bed model name
        back_populates="hospital",
        cascade="all, delete-orphan"
    )

    ambulances = relationship(
        "Ambulance",
        back_populates="hospital",
        cascade="all, delete-orphan"
    )

    bookings = relationship(
        "Booking",
        back_populates="hospital"
    )