# from sqlalchemy import ForeignKey

# from sqlalchemy import Column, Integer, String,Boolean
# from sqlalchemy.orm import relationship
# from database import Base

# class Patient(Base):
#     __tablename__ = "patients"

#     id = Column(Integer, primary_key=True)

#     user_id = Column(
#         Integer,
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True
#     )

#     full_name = Column(String(255), nullable=False)
#     age = Column(Integer)
#     blood_group = Column(String(10))
#     emergency_contact_number = Column(String(20))

#     relation = Column(String(50), nullable=True)  # only if not self
#     critical_information = Column(String, nullable=True)

#     is_self = Column(Boolean, default=True)

#     user = relationship("User", back_populates="patients")
#     bookings = relationship("Booking", back_populates="patient")


from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ----------------------------
    # Core Identity
    # ----------------------------
    full_name = Column(String(255), nullable=False)

    age = Column(Integer, nullable=True)

    blood_group = Column(String(10), nullable=True)

    emergency_contact_number = Column(String(20), nullable=True)

    # ----------------------------
    # Relationship to User
    # ----------------------------
    is_self = Column(Boolean, default=True, nullable=False)

    relation = Column(String(50), nullable=True)  # Required if is_self=False

    # ----------------------------
    # Medical Information
    # ----------------------------
    critical_information = Column(String(1000), nullable=True)

    # ----------------------------
    # Audit Tracking
    # ----------------------------
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # ----------------------------
    # Constraints
    # ----------------------------
    __table_args__ = (
        CheckConstraint("age >= 0", name="check_patient_age_positive"),
    )

    # ----------------------------
    # Relationships
    # ----------------------------
    user = relationship(
        "User",
        back_populates="patients"
    )

    bookings = relationship(
        "Booking",
        back_populates="patient"
    )