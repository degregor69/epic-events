from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = f"postgresql:{os.environ.get("DB_USER")}//{os.environ.get("DB_PASSWORD")}@localhost:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()