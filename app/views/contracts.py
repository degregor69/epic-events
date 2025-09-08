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
