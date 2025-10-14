from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Event, Client, Contract, User
from app.services.clients import ClientService
from app.services.users import UserService
from app.utils.auth import is_authenticated
from app.services.events import EventService
from app.config import get_db


@is_authenticated
def list_all_events(callback=None):
    db = next(get_db())
    events_service = EventService(db=db)
    events = events_service.get_all_events()
    if not events:
        print("⚠ Aucun événement trouvé.")
        return
    for e in events:
        print(
            f"\nID: {e.id} | Client ID: {e.client_id} | "
            f"Date de début :  {e.start_date} |  Date de fin :  {e.end_date} | Lieu : {e.location} | Support : {e.user.name}"
        )

    # TODO remove callback
    if callback:
        callback()


def list_my_events(current_user, db=None):
    db = db or next(get_db())
    service = EventService(db)
    events = service.get_my_events(current_user=current_user)
    for e in events:
        print(
            f"Événement #{e.id} | Contrat #{e.contract_id} | Client #{e.client_id} | "
            f"Date de début : {e.start_date} | Date de fin : {e.end_date or 'N/A'} | Lieu : {e.location or 'N/A'}"
        )


def list_events_without_support_view(current_user):
    db = next(get_db())
    events_service = EventService(db=db)
    events = events_service.get_events_without_support(
        current_user=current_user)

    if not events:
        print("Tous les événements ont un support assigné.")
        return

    print("Les événéments sans support assigné :")
    for e in events:
        print(
            f"Événement #{e.id} | Contrat #{e.contract_id} | Client #{e.client_id} | "
            f"Date de début : {e.start_date} | Date de fin: {e.end_date or 'N/A'} | Lieu : {e.location or 'N/A'}"
        )


def update_event_view(current_user):
    db = next(get_db())
    events_service = EventService(db=db)
    users_service = UserService(db=db)
    events = (
        events_service.get_all_events()
        if current_user.role.name == "management"
        else events_service.get_my_events(current_user)
    )
    if not events:
        print("Pas d'événement trouvé.")
        return

    print("Événements disponibles:")
    for i, e in enumerate(events, start=1):
        print(
            f"{i}. | Contrat #{e.contract_id} | Client #{e.client_id} | "
            f"Date de début : {e.start_date} | Date de fin : {e.end_date or 'N/A'} | Support: {e.user.name or 'N/A'} | Lieu : {e.location or 'N/A'}"
        )

    choice = int(input("Choisissez l'événement à modifier : ")) - 1
    event = events[choice]

    print("\nEntrez de nouvelles valeurs (laissez blanc pour ne pas modifier):")
    start_input = input(
        f"Date de début : [{event.start_date.strftime('%Y-%m-%d %H:%M')}]: ")
    end_input = input(
        f"Date de fin : [{event.end_date.strftime('%Y-%m-%d %H:%M') if event.end_date else ''}]: "
    )

    start_date = (
        datetime.strptime(
            start_input, "%Y-%m-%d %H:%M") if start_input else None
    )
    end_date = datetime.strptime(
        end_input, "%Y-%m-%d %H:%M") if end_input else None

    chosen_user_id = None
    if current_user.role.name == "management":
        users = users_service.get_all_users()
        for i, user in enumerate(users, start=1):
            print(
                f"{i}. Support: {user.name} | Role: {user.role.name}"
            )
        user_choice = int(
            input("Modifier l'utilisateur attribué (numéro) : ")) - 1
        chosen_user_id = users[user_choice].id

    location = input(f"Lieu [{event.location or ''}]: ") or None
    attendees_input = input(f"Nombre d'invités [{event.attendees or ''}]: ")
    attendees = int(attendees_input) if attendees_input else None
    notes = input(f"Notes [{event.notes or ''}]: ") or None

    contract_input = input(f"Id du contrat : [{event.contract_id}]: ")
    contract_id = int(contract_input) if contract_input else None
    client_input = input(f"Id du client : [{event.client_id}]: ")
    client_id = int(client_input) if client_input else None

    updated_event = events_service.update_event(
        current_user=current_user,
        event_id=event.id,
        user_id=chosen_user_id,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        contract_id=contract_id,
        client_id=client_id,
    )

    print("\nÉvénement mis à jour avec succès !")
    print(
        f"Événement #{updated_event.id} | Contrat #{updated_event.contract_id} | Client #{updated_event.client_id} | "
        f"Date de début: {updated_event.start_date} | Date de fin : {updated_event.end_date or 'N/A'} | "
        f"Support: {updated_event.user.name or 'N/A'} | Localisation : {updated_event.location or 'N/A'} | Nombre d'invités: {updated_event.attendees or 'N/A'}"
    )


def create_event_view(current_user: User):
    db = next(get_db())
    clients_service = ClientService(db=db)
    events_service = EventService(db=db)
    users_service = UserService(db=db)

    clients = clients_service.get_clients_with_signed_contracts(
        user_id=current_user.id)
    if not clients:
        print(f"Pas de contrats signés par {current_user.name}.")
        return

    contracts = []
    print("Contrats disponibles pour les clients dont vous êtes responsable :")
    for client in clients:
        for i, contract in enumerate(client.contracts, start=1):
            contracts.append(contract)
            print(
                f"{i}. Contrat #{contract.id} | "
                f"Client: {client.full_name} | "
                f"Total: {contract.total_amount}"
            )

    if not contracts:
        print("Pas de contrats trouvés !")
        return

    contract_choice = int(input("Choisissez un contrat (numéro) ")) - 1

    contract = contracts[contract_choice]
    client = contract.client

    start_date_str = input("Entrez la date de début (YYYY-MM-DD HH:MM): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")

    end_date_str = input(
        "Entrez la date de fin : (YYYY-MM-DD HH:MM, leave blank if none): ")
    end_date = (
        datetime.strptime(
            end_date_str, "%Y-%m-%d %H:%M") if end_date_str else None
    )
    location = input("Lieu : ") or None
    attendees_input = input("Nombre d'invités : ")
    attendees = int(attendees_input) if attendees_input else None

    users = users_service.get_all_users()
    print("Utilisateurs disponibles :")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.name} ({user.email})")
    user_choice = int(input("Choisissez l'utilisateur (numéro) : ")) - 1
    user_id = users[user_choice].id

    notes = input("Notes (optionnel): ") or None

    event = events_service.create_event(
        current_user=current_user,
        contract_id=contract.id,
        client_id=client.id,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
    )

    print("\nÉvénement créé avec succès")
    print(
        f"Événement #{event.id} | Contrat: {contract.id} | Client: {client.full_name} | "
        f"Date de début: {event.start_date} | Date de fin : {event.end_date or 'N/A'} | "
        f"| Lieu: {event.location or 'N/A'}"
    )
