# from sqlalchemy import Column, Integer, String, Boolean
# from database import Base

# class Ambulance(Base):
#     __tablename__ = "ambulances"

#     id = Column(Integer, primary_key=True, index=True)
#     hospital_id = Column(Integer)
#     driver_name = Column(String)
#     available = Column(Boolean, default=True)


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# class Ambulance(Base):
#     __tablename__ = "ambulances"

#     id = Column(Integer, primary_key=True, index=True)

#     hospital_id = Column(
#         Integer,
#         ForeignKey("hospitals.id", ondelete="CASCADE"),
#         nullable=False
#     )

#     driver_name = Column(String)
#     available = Column(Boolean, default=True)

#     hospital = relationship("Hospital", back_populates="ambulances")
#     bookings = relationship("Booking", back_populates="ambulance")


class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True)

    hospital_id = Column(
        Integer,
        ForeignKey("hospitals.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    driver_name = Column(String(255))
    driver_phone = Column(String(20))

    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)

    available = Column(Boolean, default=True)

    hospital = relationship("Hospital", back_populates="ambulances")
    bookings = relationship("Booking", back_populates="ambulance")