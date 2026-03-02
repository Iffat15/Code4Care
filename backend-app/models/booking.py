from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from database import Base
from datetime import datetime


# # # # Now bookings start as pending.
# # # class Booking(Base):
# # #     __tablename__ = "bookings"

# # #     id = Column(Integer, primary_key=True, index=True)
# # #     patient_name = Column(String)
# # #     hospital_id = Column(Integer, ForeignKey("hospitals.id"))
# # #     severity = Column(String)

# # #     ambulance_requested = Column(Boolean, default=False)
# # #     ambulance_id = Column(Integer, ForeignKey("ambulances.id"), nullable=True)
# # #     approved_at = Column(DateTime, nullable=True)
# # #     status = Column(String, default="pending")
# # #     # pending | approved | rejected


from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

import enum
from sqlalchemy import Enum


# # class BookingStatus(str, enum.Enum):
# #     pending = "pending"
# #     approved = "approved"
# #     rejected = "rejected"
# #     cancelled = "cancelled"
# #     completed = "completed"

# # class Booking(Base):
# #     __tablename__ = "bookings"

# #     id = Column(Integer, primary_key=True, index=True)

# #     hospital_id = Column(
# #         Integer,
# #         ForeignKey("hospitals.id", ondelete="CASCADE"),
# #         nullable=False
# #     )

# #     ambulance_id = Column(
# #         Integer,
# #         ForeignKey("ambulances.id", ondelete="SET NULL"),
# #         nullable=True
# #     )
    
# #     user_id = Column(
# #     Integer,
# #     ForeignKey("users.id", ondelete="CASCADE"),
# #     nullable=False,
# #     index=True
# #     )

# #     user = relationship("User", back_populates="bookings")

# #     patient_name = Column(String)
# #     severity = Column(String)
# #     ambulance_requested = Column(Boolean, default=False)
# #     approved_at = Column(DateTime(timezone=True))
# #     # status = Column(String, default="pending")
    
# #     status = Column(
# #     Enum(BookingStatus, name="booking_status"),
# #     default=BookingStatus.pending,
# #     nullable=False
# #     )

# #     hospital = relationship("Hospital", back_populates="bookings")
# #     ambulance = relationship("Ambulance", back_populates="bookings")

# import enum
# from datetime import datetime
# from sqlalchemy import (
#     Column, Integer, String, Boolean,
#     DateTime, ForeignKey, Enum
# )
# from sqlalchemy.orm import relationship
# from database import Base


# class BookingStatus(str, enum.Enum):
#     pending = "pending"
#     approved = "approved"
#     rejected = "rejected"
#     cancelled = "cancelled"
#     completed = "completed"


# class Booking(Base):
#     __tablename__ = "bookings"

#     id = Column(Integer, primary_key=True, index=True)

#     hospital_id = Column(
#         Integer,
#         ForeignKey("hospitals.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True
#     )

#     ambulance_id = Column(
#         Integer,
#         ForeignKey("ambulances.id", ondelete="SET NULL"),
#         nullable=True,
#         index=True
#     )

#     user_id = Column(
#         Integer,
#         ForeignKey("users.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True
#     )

#     patient_name = Column(String(255), nullable=False)

#     severity = Column(String(50), nullable=False)

#     ambulance_requested = Column(Boolean, default=False)

#     status = Column(
#         Enum(BookingStatus, name="booking_status"),
#         default=BookingStatus.pending,
#         nullable=False,
#         index=True
#     )

#     created_at = Column(
#         DateTime(timezone=True),
#         default=datetime.utcnow,
#         nullable=False
#     )

#     approved_at = Column(DateTime(timezone=True), nullable=True)

#     # Relationships
#     user = relationship("User", back_populates="bookings")
#     hospital = relationship("Hospital", back_populates="bookings")
#     ambulance = relationship("Ambulance", back_populates="bookings")


class BookingStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"
    completed = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    ambulance_id = Column(
        Integer,
        ForeignKey("ambulances.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    severity = Column(String(50), nullable=False)
    ambulance_requested = Column(Boolean, default=False)

    user_latitude = Column(String)
    user_longitude = Column(String)

    status = Column(
        Enum(BookingStatus, name="booking_status"),
        default=BookingStatus.pending,
        nullable=False,
        index=True
    )

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    approved_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="bookings")
    patient = relationship("Patient", back_populates="bookings")
    hospital = relationship("Hospital", back_populates="bookings")
    ambulance = relationship("Ambulance", back_populates="bookings")