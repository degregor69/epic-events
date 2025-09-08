from sqlalchemy.orm import Session
from app.models import Event


def get_all_events(db: Session):
    return db.query(Event).all()
