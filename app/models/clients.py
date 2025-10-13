from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from app.config import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    company = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    internal_contact_id = Column(
        Integer, ForeignKey("users.id"), nullable=False)
    internal_contact = relationship("User", back_populates="clients")

    contracts = relationship("Contract", back_populates="client")
