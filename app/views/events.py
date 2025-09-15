from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Event, Client, Contract, User
from app.utils.auth import is_authenticated
from app.controllers.events import (
    get_all_events,
    get_events_without_support,
    update_event,
    create_event,
)
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


def update_event_view(current_user):
    db = next(get_db())

    events = db.query(Event).all()
    if not events:
        print("❌ No events found.")
        return

    print("Available events:")
    for i, e in enumerate(events, start=1):
        print(
            f"{i}. Event #{e.id} | Contract #{e.contract_id} | Client #{e.client_id} | "
            f"Start: {e.start_date} | End: {e.end_date or 'N/A'} | Support: {e.support_contact or 'N/A'} | Location: {e.location or 'N/A'}"
        )

    choice = int(input("Choose event (number): ")) - 1
    event = events[choice]

    print("\nEnter new values (leave blank to keep current):")
    start_input = input(f"Start date [{event.start_date.strftime('%Y-%m-%d %H:%M')}]: ")
    end_input = input(
        f"End date [{event.end_date.strftime('%Y-%m-%d %H:%M') if event.end_date else ''}]: "
    )

    start_date = (
        datetime.strptime(start_input, "%Y-%m-%d %H:%M") if start_input else None
    )
    end_date = datetime.strptime(end_input, "%Y-%m-%d %H:%M") if end_input else None

    support_contact = (
        input(f"Support contact [{event.support_contact or ''}]: ") or None
    )
    location = input(f"Location [{event.location or ''}]: ") or None
    attendees_input = input(f"Attendees [{event.attendees or ''}]: ")
    attendees = int(attendees_input) if attendees_input else None
    notes = input(f"Notes [{event.notes or ''}]: ") or None

    contract_input = input(f"Contract ID [{event.contract_id}]: ")
    contract_id = int(contract_input) if contract_input else None
    client_input = input(f"Client ID [{event.client_id}]: ")
    client_id = int(client_input) if client_input else None

    updated_event = update_event(
        current_user=current_user,
        db=db,
        event_id=event.id,
        start_date=start_date,
        end_date=end_date,
        support_contact=support_contact,
        location=location,
        attendees=attendees,
        notes=notes,
        contract_id=contract_id,
        client_id=client_id,
    )

    print("\n✅ Event updated successfully!")
    print(
        f"Event #{updated_event.id} | Contract #{updated_event.contract_id} | Client #{updated_event.client_id} | "
        f"Start: {updated_event.start_date} | End: {updated_event.end_date or 'N/A'} | "
        f"Support: {updated_event.support_contact or 'N/A'} | Location: {updated_event.location or 'N/A'} | Attendees: {updated_event.attendees or 'N/A'}"
    )


def get_clients_with_signed_contracts(db: Session, user_id: int):
    clients = (
        db.query(Client)
        .join(Contract, Contract.client_id == Client.id)
        .filter(Client.internal_contact_id == user_id)
        .filter(Contract.signed.is_(True))
        .all()
    )
    return clients


def create_event_view(current_user: User):
    db = next(get_db())

    clients = get_clients_with_signed_contracts(db=db, user_id=current_user.id)
    if not clients:
        print(f"❌ No clients with signed contracts for the user {current_user.name}.")
        return

    contracts = []
    print("Available contracts:")
    for client in clients:
        for contract in client.contracts:
            contracts.append(contract)
            print(
                f"{len(contracts)}. Contract #{contract.id} | "
                f"Client: {client.full_name} | "
                f"Total: {contract.total_amount}"
            )

    if not contracts:
        print("❌ No signed contracts found.")
        return

    contract_choice = int(input("Choose contract (number): ")) - 1
    if contract_choice < 0 or contract_choice >= len(contracts):
        print("❌ Invalid choice.")
        return

    contract = contracts[contract_choice]
    client = contract.client

    start_date_str = input("Enter start date (YYYY-MM-DD HH:MM): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")

    end_date_str = input("Enter end date (YYYY-MM-DD HH:MM, leave blank if none): ")
    end_date = (
        datetime.strptime(end_date_str, "%Y-%m-%d %H:%M") if end_date_str else None
    )

    support_contact = input("Support contact (optional): ") or None
    location = input("Location (optional): ") or None
    attendees_input = input("Number of attendees (optional): ")
    attendees = int(attendees_input) if attendees_input else None
    notes = input("Notes (optional): ") or None

    event = create_event(
        current_user=current_user,
        db=db,
        contract_id=contract.id,
        client_id=client.id,
        start_date=start_date,
        end_date=end_date,
        support_contact=support_contact,
        location=location,
        attendees=attendees,
        notes=notes,
    )

    print("\n✅ Event created successfully!")
    print(
        f"Event #{event.id} | Contract: {contract.id} | Client: {client.full_name} | "
        f"Start: {event.start_date} | End: {event.end_date or 'N/A'} | "
        f"Support: {event.support_contact or 'N/A'} | Location: {event.location or 'N/A'}"
    )
