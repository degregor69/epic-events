from app.models import User, Client
from app.utils.auth import is_authenticated
from app.services.clients import ClientService
from app.config import get_db


@is_authenticated
def list_all_clients():
    db = next(get_db())
    clients_service = ClientService(db=db)
    clients = clients_service.get_all_clients()
    if not clients:
        print("⚠ Aucun client trouvé.")
        return
    for c in clients:
        print(
            f"\nID: {c.id} | Nom: {c.full_name} | Email: {c.email} | Entreprise: {c.company}"
        )


def create_client_view(current_user: User):
    db = next(get_db())
    clients_service = ClientService(db=db)

    print("Enter new client information:")

    full_name = input("Full name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    company = input("Company: ")

    client = clients_service.create_client(
        current_user=current_user,
        full_name=full_name,
        email=email,
        phone=phone,
        company=company,
    )

    print("\n✅ Client created successfully!")
    print(
        f"Client #{client.id} | Name: {client.full_name} | Email: {client.email} | "
        f"Phone: {client.phone} | Company: {client.company} | Internal contact: {client.internal_contact}"
    )


def update_client_view(current_user):
    db = next(get_db())
    clients_service = ClientService(db=db)

    clients = clients_service.get_clients_by_user(user_id=current_user.id)
    if not clients:
        print("❌ You are not responsible for any clients.")
        return

    print("Your clients:")
    for i, client in enumerate(clients, start=1):
        print(
            f"{i}. Client #{client.id} | Name: {client.full_name} | Email: {client.email} | "
            f"Phone: {client.phone} | Company: {client.company}"
        )

    choice = int(input("Choose client (number): ")) - 1
    client = clients[choice]

    print("\nEnter new values (leave blank to keep current):")
    full_name = input(f"Full name [{client.full_name}]: ") or None
    email = input(f"Email [{client.email}]: ") or None
    phone = input(f"Phone [{client.phone}]: ") or None
    company = input(f"Company [{client.company}]: ") or None

    change_internal = input(f"Change responsible user? (y/N): ").lower() == "y"
    internal_contact_id = None
    if change_internal:
        users = db.query(User).all()
        print("Available users:")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user.name} ({user.email})")
        user_choice = int(input("Choose user (number): ")) - 1
        internal_contact_id = users[user_choice].id

    updated_client = clients_service.update_client(
        current_user=current_user,
        client_id=client.id,
        full_name=full_name,
        email=email,
        phone=phone,
        company=company,
        internal_contact_id=internal_contact_id,
    )

    print("\n✅ Client updated successfully!")
    print(
        f"Client #{updated_client.id} | Name: {updated_client.full_name} | Email: {updated_client.email} | "
        f"Phone: {updated_client.phone} | Company: {updated_client.company} | Responsible: {updated_client.internal_contact.name}"
    )
