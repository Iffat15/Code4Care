from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer)
    driver_name = Column(String)
    available = Column(Boolean, default=True)