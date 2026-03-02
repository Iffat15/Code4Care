# from sqlalchemy import Column, Integer, String
# from database import Base

# class Hospital(Base):
#     __tablename__ = "hospitals"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     location = Column(String, nullable=False)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


# class Hospital(Base):
#     __tablename__ = "hospitals"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     location = Column(String, nullable=False)

#     # Relationships
#     beds = relationship("Bed", back_populates="hospital", cascade="all, delete")
#     ambulances = relationship("Ambulance", back_populates="hospital", cascade="all, delete")
#     bookings = relationship("Booking", back_populates="hospital", cascade="all, delete")

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)

    rating = Column(String(10))

    beds = relationship("BedInventory", back_populates="hospital", cascade="all, delete")
    ambulances = relationship("Ambulance", back_populates="hospital", cascade="all, delete")
    bookings = relationship("Booking", back_populates="hospital")