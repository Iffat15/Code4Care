from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    bed_type = Column(String)  # ICU / General
    available = Column(Integer, default=0)