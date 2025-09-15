from app.utils.auth import is_authenticated
from app.utils.permissions import is_support
from app.controllers.events import get_all_events, get_events_without_support
from app.config import get_db


@is_authenticated
def list_all_events(callback=None):
    db = next(get_db())
    events = get_all_events(db)
    if not events:
        print("⚠ Aucun événement trouvé.")
        return
    for e in events:
        print(
            f"\nID: {e.id} | Client ID: {e.client_id} | "
            f"Start date :  {e.start_date} |  End date :  {e.end_date} | Location : {e.location} | Support ID: {e.support_contact}"
        )

    if callback:
        callback()


def list_events_without_support_view(current_user):
    db = next(get_db())
    events = get_events_without_support(current_user=current_user, db=db)

    if not events:
        print("✅ All events have a support assigned.")
        return

    print("📅 Events without support:")
    for e in events:
        print(
            f"Event #{e.id} | Contract #{e.contract_id} | Client #{e.client_id} | "
            f"Start: {e.start_date} | End: {e.end_date or 'N/A'} | Location: {e.location or 'N/A'}"
        )
