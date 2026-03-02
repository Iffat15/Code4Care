from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class NGO(Base):
    __tablename__ = "ngos"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    contact_number = Column(String(20), nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationship with Ambulance
    ambulances = relationship(
        "Ambulance",
        back_populates="ngo"
    )