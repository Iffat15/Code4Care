# from sqlalchemy import Column, Integer, ForeignKey, String
# from sqlalchemy.orm import relationship
# from database import Base

# class Bed(Base):
#     __tablename__ = "beds"

#     id = Column(Integer, primary_key=True, index=True)
#     hospital_id = Column(Integer, ForeignKey("hospitals.id"))
#     bed_type = Column(String)  # ICU / General
#     available = Column(Integer, default=0)

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# class Bed(Base):
#     __tablename__ = "beds"

#     id = Column(Integer, primary_key=True, index=True)

#     hospital_id = Column(
#         Integer,
#         ForeignKey("hospitals.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     bed_type = Column(String)
#     available = Column(Integer, default=0)

#     # Relationship
#     hospital = relationship("Hospital", back_populates="beds")

class BedInventory(Base):
    __tablename__ = "bed_inventory"

    id = Column(Integer, primary_key=True)

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    bed_type = Column(String(50), nullable=False)  # ICU, Emergency, General
    total_beds = Column(Integer, nullable=False)
    available_beds = Column(Integer, nullable=False)

    hospital = relationship("Hospital", back_populates="beds")