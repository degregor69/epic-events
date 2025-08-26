import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from app.config import Base


class TeamEnum(enum.Enum):
    commercial = "commercial"
    support = "support"
    management = "management"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    team = Column(Enum(TeamEnum), nullable=False)