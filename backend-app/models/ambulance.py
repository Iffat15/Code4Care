import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Index
)
from sqlalchemy.orm import relationship
from database import Base


# ---------------------------------------------------------
# Ambulance Status Enum (State Machine)
# ---------------------------------------------------------
class AmbulanceStatus(str, enum.Enum):
    available = "available"
    assigned = "assigned"
    en_route = "en_route"
    at_scene = "at_scene"
    transporting = "transporting"
    maintenance = "maintenance"


class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True, index=True)

    # ----------------------------
    # Ownership
    # ----------------------------
    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    ngo_id = Column(
        Integer,
        ForeignKey("ngos.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # ----------------------------
    # Driver Info
    # ----------------------------
    driver_name = Column(String(255), nullable=True)
    driver_phone = Column(String(20), nullable=True)

    # ----------------------------
    # Location Tracking
    # ----------------------------
    latitude = Column(Float, nullable=True, index=True)
    longitude = Column(Float, nullable=True, index=True)

    # ----------------------------
    # Status Lifecycle
    # ----------------------------
    status = Column(
        Enum(AmbulanceStatus, name="ambulance_status"),
        default=AmbulanceStatus.available,
        nullable=False,
        index=True
    )

    last_updated = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ----------------------------
    # Relationships
    # ----------------------------
    hospital = relationship(
        "Hospital",
        back_populates="ambulances"
    )

    ngo = relationship(
        "NGO",
        back_populates="ambulances"
    )

    bookings = relationship(
        "Booking",
        back_populates="ambulance"
    )

    # ----------------------------
    # Index Optimization
    # ----------------------------
    __table_args__ = (
        Index("idx_ambulance_status_location", "status", "latitude", "longitude"),
    )