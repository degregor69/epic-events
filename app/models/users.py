import enum
from sqlalchemy import Column, Integer, String, Enum
from app.config import Base


class TeamEnum(enum.Enum):
    commercial = "commercial"
    support = "support"
    management = "management"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    team = Column(Enum(TeamEnum), nullable=False)
