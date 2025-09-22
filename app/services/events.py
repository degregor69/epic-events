from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Event, User
from app.utils.permissions import is_management, is_sales
from app.databases.events import EventDB


class EventService:
    def __init__(self, db: Session):
        self.event_db = EventDB(db)

    def get_all_events(self):
        return self.event_db.get_all()

    @is_management
    def get_events_without_support(self, current_user: User):
        return self.event_db.get_without_support()

    @is_management
    def update_event(
        self,
        current_user: User,
        event_id: int,
        start_date: datetime = None,
        end_date: datetime = None,
        support_contact: str = None,
        location: str = None,
        attendees: int = None,
        notes: str = None,
        contract_id: int = None,
        client_id: int = None,
    ):
        event = self.event_db.get_by_id(event_id)
        if not event:
            raise Exception(f"❌ Event with id {event_id} not found")

        data = {
            "start_date": start_date,
            "end_date": end_date,
            "support_contact": support_contact,
            "location": location,
            "attendees": attendees,
            "notes": notes,
            "contract_id": contract_id,
            "client_id": client_id,
        }
        return self.event_db.update(event, data)

    @is_sales
    def create_event(
        self,
        current_user: User,
        contract_id: int,
        client_id: int,
        start_date: datetime,
        end_date: datetime = None,
        support_contact: str = None,
        location: str = None,
        attendees: int = None,
        notes: str = None,
    ):
        event = Event(
            contract_id=contract_id,
            client_id=client_id,
            start_date=start_date,
            end_date=end_date,
            support_contact=support_contact,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        return self.event_db.add(event)
