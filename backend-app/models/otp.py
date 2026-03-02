from sqlalchemy import ForeignKey

from sqlalchemy import Column, Integer, String,Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base


class OTP(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True)

    phone_number = Column(String(20), index=True, nullable=False)
    otp_code = Column(String(6), nullable=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    verified = Column(Boolean, default=False)