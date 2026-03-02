# from sqlalchemy import Column, Integer, String
# from database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String, unique=True)
#     role = Column(String)  # patient or admin


import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# -------------------------------
# User Role Enum (PostgreSQL ENUM)
# -------------------------------
class UserRole(str, enum.Enum):
    patient = "patient"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(Enum(UserRole, name="user_roles"), default=UserRole.patient)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    bookings = relationship("Booking", back_populates="user")