import pytest

from app.controllers.events import get_all_events, get_events_without_support


def test_get_all_events(db, events):
    db_events = get_all_events(db)

    assert len(db_events) == len(events)


def test_get_events_without_support(db, management_user, events):
    events[0].support_contact = None
    events[1].support_contact = "John Doe"
    db.commit()

    result = get_events_without_support(current_user=management_user, db=db)

    assert result is not None
    assert all(e.support_contact is None for e in result)
    assert events[0] in result
    assert events[1] not in result


def test_get_events_without_support_with_non_authorized_user(db, support_user, events):
    events[0].support_contact = None
    events[1].support_contact = "John Doe"
    db.commit()

    with pytest.raises(Exception) as exc:
        result = get_events_without_support(current_user=support_user, db=db)
        assert str(exc.value) == "Accès refusé (réservé au Management)"
