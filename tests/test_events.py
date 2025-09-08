from app.controllers.events import get_all_events


def test_get_all_events(db, events):
    db_events = get_all_events(db)

    assert len(db_events) == len(events)
