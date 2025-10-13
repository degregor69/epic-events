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

    print("Entrez les informations du nouveau client :")

    full_name = input("Nom complet : ")
    email = input("Email : ")
    phone = input("Téléphone : ")
    company = input("Entreprise :")

    client = clients_service.create_client(
        current_user=current_user,
        full_name=full_name,
        email=email,
        phone=phone,
        company=company,
    )

    print("\nClient créé avec succès !")
    print(
        f"Client #{client.id} | Nom : {client.full_name} | Email : {client.email} | "
        f"Téléphone : {client.phone} | Entreprise : {client.company} | Contact interne : {client.internal_contact.name}"
    )


def update_client_view(current_user):
    db = next(get_db())
    clients_service = ClientService(db=db)

    clients = clients_service.get_clients_by_user(user_id=current_user.id)
    if not clients:
        print("Vous n'êtes responsables d'aucun client")
        return

    print("Vos clients : ")
    for i, client in enumerate(clients, start=1):
        print(
            f"{i}. Client #{client.id} | Nom : {client.full_name} | Email : {client.email} | "
            f"Téléphone : {client.phone} | Entreprise : {client.company}"
        )

    choice = int(input("Choissiez le client à modifier (numéro) ")) - 1
    client = clients[choice]

    print("\nEntrez les nouvelles valeurs (laissez blanc pour passer):")
    full_name = input(f"Nom complet [{client.full_name}]: ") or None
    email = input(f"Email [{client.email}]: ") or None
    phone = input(f"Téléphone [{client.phone}]: ") or None
    company = input(f"Entreprise [{client.company}]: ") or None

    change_internal = input(
        f"Changez le responsable du client (o/N): ").lower() == "o"
    internal_contact_id = None
    if change_internal:
        users = db.query(User).all()
        print("Utilisateurs disponibles :")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user.name} ({user.email})")
        user_choice = int(
            input("Choisissez l'utilisateur disponible (numéro) :")) - 1
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

    print("\nClient mis à jour avec succès !")
    print(
        f"Client #{updated_client.id} | Nom : {updated_client.full_name} | Email : {updated_client.email} | "
        f"Téléphone : {updated_client.phone} | Entreprise : {updated_client.company} | Responsable : {updated_client.internal_contact.name}"
    )
