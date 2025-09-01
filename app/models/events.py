from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from app.config import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    support_contact = Column(String, nullable=True)
    location = Column(String, nullable=True)
    attendees = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
