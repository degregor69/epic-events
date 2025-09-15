from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from app.models import Event, User
from app.utils.permissions import is_management


def get_all_events(db: Session):
    return db.query(Event).all()


@is_management
def get_events_without_support(current_user: User, db: Session):
    return db.query(Event).filter(Event.support_contact.is_(None)).all()


@is_management
def update_event(
    current_user: User,
    db: Session,
    event_id: int,
    start_date: DateTime = None,
    end_date: DateTime = None,
    support_contact: str = None,
    location: str = None,
    attendees: int = None,
    notes: str = None,
    contract_id: int = None,
    client_id: int = None,
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise Exception(f"❌ Event with id {event_id} not found")

    if start_date is not None:
        event.start_date = start_date
    if end_date is not None:
        event.end_date = end_date
    if support_contact is not None:
        event.support_contact = support_contact
    if location is not None:
        event.location = location
    if attendees is not None:
        event.attendees = attendees
    if notes is not None:
        event.notes = notes
    if contract_id is not None:
        event.contract_id = contract_id
    if client_id is not None:
        event.client_id = client_id

    db.commit()
    db.refresh(event)
    return event
