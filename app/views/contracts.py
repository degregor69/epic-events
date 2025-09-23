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
            f"Total: {c.total_amount} | Pending: {c.pending_amount} | Signed: {c.signed}\n"
        )


from app.config import get_db


def create_contract_view(current_user):
    db = next(get_db())
    clients_service = ClientService(db=db)
    users_service = UserService(db=db)
    contracts_service = ContractService(db=db)

    clients = clients_service.get_all_clients()
    print("Available clients:")
    for i, client in enumerate(clients, start=1):
        print(f"{i}. {client.full_name} ({client.company})")
    client_choice = int(input("Choose client (number): ")) - 1
    client_id = clients[client_choice].id

    users = users_service.get_all_users()
    print("Assign contract to user:")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.name} ({user.email})")
    user_choice = int(input("Choose user (number): ")) - 1
    user_id = users[user_choice].id

    total_amount = float(input("Enter total amount: "))
    pending_amount = float(input("Enter pending amount: "))
    signed_input = input("Is it signed? (y/N): ").lower()
    signed = signed_input == "y"

    contract = contracts_service.create_contract(
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
        print("❌ No contracts found.")
        return

    print("Available contracts:")
    for i, contract in enumerate(contracts, start=1):
        client = contract.client.full_name if contract.client else "N/A"
        print(
            f"{i}. Contract #{contract.id} | Client: {client} | "
            f"Total: {contract.total_amount} | Pending: {contract.pending_amount} | "
            f"Signed: {'✅' if contract.signed else '❌'}"
        )
    contract_choice = int(input("Choose contract (number): ")) - 1
    contract_id = contracts[contract_choice].id

    print("\nEnter new values (leave blank to keep current):")

    total_amount_input = input("New total amount: ")
    total_amount = float(total_amount_input) if total_amount_input else None

    pending_amount_input = input("New pending amount: ")
    pending_amount = float(pending_amount_input) if pending_amount_input else None

    signed_input = input("Is it signed? (y/N/leave blank to keep): ").lower()
    signed = None
    if signed_input == "y":
        signed = True
    elif signed_input == "n":
        signed = False

    change_user = input("Change assigned user? (y/N): ").lower() == "y"
    user_id = None
    if change_user:
        users = users_service.get_all_users()
        print("Available users:")
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user.name} ({user.email})")
        user_choice = int(input("Choose user (number): ")) - 1
        user_id = users[user_choice].id

    change_client = input("Change client? (y/N): ").lower() == "y"
    client_id = None
    if change_client:
        clients = clients_service.get_all_clients()
        print("Available clients:")
        for i, client in enumerate(clients, start=1):
            print(f"{i}. {client.full_name} ({client.company})")
        client_choice = int(input("Choose client (number): ")) - 1
        client_id = clients[client_choice].id

    updated_contract = contracts_service.update_contract(
        current_user=current_user,
        db=db,
        contract_id=contract_id,
        total_amount=total_amount,
        pending_amount=pending_amount,
        signed=signed,
        user_id=user_id,
        client_id=client_id,
    )

    print("\n✅ Contract updated successfully!")
    client_name = (
        updated_contract.client.full_name if updated_contract.client else "N/A"
    )
    print(
        f"Contract #{updated_contract.id} | Client: {client_name} | "
        f"Total: {updated_contract.total_amount} | Pending: {updated_contract.pending_amount} | "
        f"Signed: {'✅' if updated_contract.signed else '❌'}"
    )


def list_contracts_filtered_view(current_user):
    db = next(get_db())
    contracts_service = ContractService(db=db)

    print("Filter contracts:")
    only_unsigned = input("Show only unsigned contracts? (y/N): ").lower() == "y"
    only_pending = (
        input("Show only contracts with pending amount? (y/N): ").lower() == "y"
    )

    contracts = contracts_service.get_contracts_filtered(
        current_user=current_user,
        db=db,
        only_unsigned=only_unsigned,
        only_pending=only_pending,
    )

    if not contracts:
        print("✅ No contracts found with the selected filters.")
        return

    print("\nFiltered contracts:")
    for c in contracts:
        client_name = c.client.full_name if c.client else "N/A"
        user_name = c.user.name if c.user else "N/A"
        print(
            f"Contract #{c.id} | Client: {client_name} | Assigned to: {user_name} | "
            f"Total: {c.total_amount} | Pending: {c.pending_amount} | Signed: {'✅' if c.signed else '❌'}"
        )
