from app.controllers.contracts import get_all_contracts
from app.config import get_db
from app.utils.auth import is_authenticated


@is_authenticated
def list_all_contracts():
    db = next(get_db())
    contracts = get_all_contracts(db)

    if not contracts:
        print("⚠ Aucun contrat trouvé.")
        return

    for c in contracts:
        print(
            f"\nID: {c.id} | Client ID: {c.client_id} | User ID: {c.user_id} | "
            f"Total: {c.total_amount} | Pending: {c.pending_amount} | Signed: {c.signed}\n"
        )


from app.config import get_db
from app.controllers.contracts import create_contract
from app.controllers.users import get_all_users
from app.controllers.clients import get_all_clients


def create_contract_view(current_user):
    db = next(get_db())

    clients = get_all_clients(db)
    print("Available clients:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}. {client.full_name} ({client.company})")
    client_choice = int(input("Choose client (number): ")) - 1
    client_id = clients[client_choice].id

    users = get_all_users(db)
    print("Assign contract to user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.name} ({user.email})")
    user_choice = int(input("Choose user (number): ")) - 1
    user_id = users[user_choice].id

    total_amount = float(input("Enter total amount: "))
    pending_amount = float(input("Enter pending amount: "))
    signed_input = input("Is it signed? (y/N): ").lower()
    signed = signed_input == "y"

    contract = create_contract(
        current_user=current_user,
        db=db,
        user_id=user_id,
        client_id=client_id,
        total_amount=total_amount,
        pending_amount=pending_amount,
        signed=signed,
    )
    print(contract)

    print(
        f"✅ Contract #{contract.id} created for client {clients[client_choice].full_name}"
    )
