from app.config import get_db
from app.services.clients import ClientService
from app.services.contracts import ContractService
from app.services.users import UserService
from app.utils.auth import is_authenticated


@is_authenticated
def list_all_contracts():
    db = next(get_db())
    contracts_service = ContractService(db=db)
    contracts = contracts_service.get_all_contracts()

    if not contracts:
        print("⚠ Aucun contrat trouvé.")
        return

    for c in contracts:
        print(
            f"\nID: {c.id} | Client ID: {c.client_id} | User ID: {c.user_id} | "
            f"Total: {c.total_amount} | Pending: {c.pending_amount} | Signed: {c.signed}"
        )


def create_contract_view(current_user):
    db = next(get_db())
    clients_service = ClientService(db=db)
    users_service = UserService(db=db)
    contracts_service = ContractService(db=db)

    clients = clients_service.get_all_clients()
    print("Clients disponibles :")
    for i, client in enumerate(clients, start=1):
        print(f"{i}. {client.full_name} ({client.company})")
    client_choice = int(
        input("Choisissez un client en entrant le numéro : ")) - 1
    client_id = clients[client_choice].id

    users = users_service.get_all_users()
    print("Assignez le contrat à un utilisateur :")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.name} ({user.email})")
    user_choice = int(
        input("Choisissez l'utilisateur en entrant le numéro : ")) - 1
    user_id = users[user_choice].id

    total_amount = float(input("Entrez le montant du contrat : "))
    pending_amount = float(input("Entrez le montant restant : "))
    signed_input = input("Le contrat est-il signé ? (o/N): ").lower()
    signed = signed_input == "o"

    contract = contracts_service.create_contract(
        current_user=current_user,
        user_id=user_id,
        client_id=client_id,
        total_amount=total_amount,
        pending_amount=pending_amount,
        signed=signed,
    )

    print(
        f"Contrat #{contract.id} créé pour le client {clients[client_choice].full_name}"
    )


def update_contract_view(current_user):
    db = next(get_db())
    contracts_service = ContractService(db=db)
    users_service = UserService(db=db)
    clients_service = ClientService(db=db)

    if current_user.role.name == "management":
        contracts = contracts_service.get_all_contracts()
    else:
        contracts = contracts_service.get_all_contracts_for_clients_user(
            current_user.id
        )

    contracts = contracts_service.get_all_contracts()
    if not contracts:
        print("Pas de contrats trouvés.")
        return

    print("Contrats disponibles : ")
    for i, contract in enumerate(contracts, start=1):
        print(
            f"{i}. | Client: {contract.client.full_name} | "
            f"Total : {contract.total_amount} | Restant : {contract.pending_amount} | "
            f"Signed : {"Oui" if contract.signed else "Non"}"
        )
    contract_choice = int(input("Choisissez le numéro de contrat : ")) - 1
    contract_id = contracts[contract_choice].id

    print("\nEntrez les nouvelles valeurs (laissez blanc pour passer):")

    total_amount_input = input("Nouveau montant total : ")
    total_amount = float(total_amount_input) if total_amount_input else None

    pending_amount_input = input("Nouveau montant restant : ")
    pending_amount = float(
        pending_amount_input) if pending_amount_input else None

    signed_input = input("Est-ce signé ? (o/N): ").lower()
    signed = None
    if signed_input == "o":
        signed = True
    elif signed_input == "n":
        signed = False

    change_user = input(
        "Voulez-vous modifier l'utilisateur assigné (o/N): ").lower() == "o"
    user_id = None
    if change_user:
        users = users_service.get_all_users()
        print("Utilisateurs disponibles :")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user.name} ({user.email})")
        user_choice = int(input("Choisissez l'utilisateur (numéro) : ")) - 1
        user_id = users[user_choice].id

    change_client = input(
        "Voulez-vous changer le client ? (o/N): ").lower() == "y"
    client_id = None
    if change_client:
        clients = clients_service.get_all_clients()
        print("Clients disponibles :")
        for i, client in enumerate(clients, start=1):
            print(f"{i}. {client.full_name} ({client.company})")
        client_choice = int(input("Choisissez le client (numéro) : ")) - 1
        client_id = clients[client_choice].id

    updated_contract = contracts_service.update_contract(
        current_user=current_user,
        contract_id=contract_id,
        total_amount=total_amount,
        pending_amount=pending_amount,
        signed=signed,
        user_id=user_id,
        client_id=client_id,
    )

    print("\n Contraté modifié avec succès !")
    client_name = (
        updated_contract.client.full_name if updated_contract.client else "N/A"
    )
    print(
        f"Contrat #{updated_contract.id} | Client: {client_name} | "
        f"Total: {updated_contract.total_amount} | Restant : {updated_contract.pending_amount} | "
        f"Signed: {"Oui" if updated_contract.signed else "Non"}"
    )


def list_contracts_filtered_view(current_user):
    db = next(get_db())
    contracts_service = ContractService(db=db)

    print("Voulez-vous filtrer les contrats ?:")
    only_unsigned = input(
        "Montrer seulement les contrats signés ? (o/N): ").lower() == "o"
    only_pending = (
        input(
            "Montrer seulement les contrats avec un montant restant (o/N): ").lower() == "o"
    )

    contracts = contracts_service.get_contracts_filtered(
        current_user=current_user,
        only_unsigned=only_unsigned,
        only_pending=only_pending,
    )

    if not contracts:
        print("Pas de contrats trouvés avec ces filtres.")
        return

    print("\nContrats :")
    for c in contracts:
        client_name = c.client.full_name if c.client else "N/A"
        user_name = c.user.name if c.user else "N/A"
        print(
            f"Contrat #{c.id} | Client: {client_name} | Assigné à : {user_name} | "
            f"Total: {c.total_amount} | Restant : {c.pending_amount} | Signé : {"Oui" if c.signed else "Non"}"
        )
