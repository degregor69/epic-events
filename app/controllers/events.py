from sqlalchemy.orm import Session
from app.models import Event, User
from app.utils.permissions import is_management


def get_all_events(db: Session):
    return db.query(Event).all()


@is_management
def get_events_without_support(current_user: User, db: Session):
    return db.query(Event).filter(Event.support_contact.is_(None)).all()
