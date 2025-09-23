from sqlalchemy.orm import Session
from app.models import Event


class EventDB:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Event).all()

    def get_without_support(self):
        return self.db.query(Event).filter(Event.user_id.is_(None)).all()

    def get_by_id(self, event_id: int):
        return self.db.query(Event).filter(Event.id == event_id).first()

    def add(self, event: Event):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update(self, event: Event, data: dict):
        for field, value in data.items():
            if hasattr(event, field) and value is not None:
                setattr(event, field, value)
        self.db.commit()
        self.db.refresh(event)
        return event
