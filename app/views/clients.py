from app.models import User
from app.utils.auth import is_authenticated
from app.controllers.clients import get_all_clients, create_client
from app.config import get_db


@is_authenticated
def list_all_clients():
    db = next(get_db())
    clients = get_all_clients(db)
    if not clients:
        print("⚠ Aucun client trouvé.")
        return
    for c in clients:
        print(
            f"\nID: {c.id} | Nom: {c.full_name} | Email: {c.email} | Entreprise: {c.company}"
        )


def create_client_view(current_user: User):
    db = next(get_db())

    print("Enter new client information:")

    full_name = input("Full name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    company = input("Company: ")

    client = create_client(
        current_user=current_user,
        db=db,
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
