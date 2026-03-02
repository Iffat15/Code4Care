from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base


class Bed(Base):
    __tablename__ = "bed_inventory"

    id = Column(Integer, primary_key=True, index=True)

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ICU | Emergency | General
    bed_type = Column(String(50), nullable=False, index=True)

    total_beds = Column(Integer, nullable=False)

    available_beds = Column(Integer, nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ----------------------------
    # Constraints
    # ----------------------------
    __table_args__ = (

        # Prevent duplicate bed types per hospital
        UniqueConstraint(
            "hospital_id",
            "bed_type",
            name="uq_hospital_bedtype"
        ),

        # Prevent negative values
        CheckConstraint(
            "total_beds >= 0",
            name="check_total_beds_positive"
        ),

        CheckConstraint(
            "available_beds >= 0",
            name="check_available_beds_positive"
        ),

        # Prevent available > total
        CheckConstraint(
            "available_beds <= total_beds",
            name="check_available_le_total"
        ),
    )

    # ----------------------------
    # Relationships
    # ----------------------------
    hospital = relationship(
        "Hospital",
        back_populates="beds"
    )