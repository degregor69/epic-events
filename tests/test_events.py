from datetime import datetime

import pytest

from app.services.events import EventService
from app.models import Event


def test_get_all_events(db, events):
    events_service = EventService(db=db)
    db_events = events_service.get_all_events()

    assert len(db_events) == len(events)


def test_get_events_without_support(db, management_user, events):
    events[0].support_contact = None
    events[1].support_contact = "John Doe"
    db.commit()

    events_service = EventService(db=db)
    result = events_service.get_events_without_support(
        current_user=management_user,
    )

    assert result is not None
    assert all(e.support_contact is None for e in result)
    assert events[0] in result
    assert events[1] not in result


def test_get_events_without_support_with_non_authorized_user(db, support_user, events):
    events[0].support_contact = None
    events[1].support_contact = "John Doe"
    db.commit()

    with pytest.raises(Exception) as exc:
        events_service = EventService(db=db)
        result = events_service.get_events_without_support(
            current_user=support_user,
        )
        assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_update_event(db, management_user, events, clients):
    event = events[0]
    events_service = EventService(db=db)

    updated_event = events_service.update_event(
        current_user=management_user,
        event_id=event.id,
        start_date=event.start_date.replace(hour=14, minute=0),
        end_date=event.end_date.replace(hour=16, minute=0) if event.end_date else None,
        support_contact="Jane Doe",
        location="New Location",
        attendees=50,
        notes="Updated notes",
        contract_id=event.contract_id,
        client_id=clients[1].id,
    )

    assert updated_event is not None

    db_updated_event: Event = db.get(Event, event.id)

    assert db_updated_event.id == event.id
    assert db_updated_event.start_date.hour == 14
    if db_updated_event.end_date:
        assert db_updated_event.end_date.hour == 16
    assert db_updated_event.support_contact == "Jane Doe"
    assert db_updated_event.location == "New Location"
    assert db_updated_event.attendees == 50
    assert db_updated_event.notes == "Updated notes"
    assert db_updated_event.contract_id == event.contract_id
    assert db_updated_event.client_id == clients[1].id


def test_update_event_with_non_authorized_user(db, support_user, events, clients):
    with pytest.raises(Exception) as exc:
        event = events[0]
        events_service = EventService(db=db)
        updated_event = events_service.update_event(
            current_user=support_user,
            event_id=event.id,
            start_date=event.start_date.replace(hour=14, minute=0),
            end_date=(
                event.end_date.replace(hour=16, minute=0) if event.end_date else None
            ),
            support_contact="Jane Doe",
            location="New Location",
            attendees=50,
            notes="Updated notes",
            contract_id=event.contract_id,
            client_id=clients[1].id,
        )
        assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_create_event(db, sales_user, clients, contracts):
    client = clients[0]
    client.internal_contact_id = sales_user.id
    db.commit()

    contract = contracts[0]
    contract.client_id = client.id
    contract.signed = True
    db.commit()

    events_service = EventService(db=db)
    event = events_service.create_event(
        current_user=sales_user,
        contract_id=contract.id,
        client_id=client.id,
        start_date=datetime(2025, 1, 1, 10, 0),
        end_date=datetime(2025, 1, 1, 12, 0),
        support_contact="John Doe",
        location="Paris",
        attendees=50,
        notes="Kickoff meeting",
    )
    assert event is not None
    assert event.contract_id == contract.id
    assert event.client_id == client.id
    assert event.start_date == datetime(2025, 1, 1, 10, 0)
    assert event.end_date == datetime(2025, 1, 1, 12, 0)
    assert event.support_contact == "John Doe"
    assert event.location == "Paris"
    assert event.attendees == 50
    assert event.notes == "Kickoff meeting"

    db_event = db.get(Event, event.id)
    assert db_event is not None
