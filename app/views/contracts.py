from app.controllers.contracts import get_all_contracts
from app.config import get_db
from app.models import User
from app.utils.permissions import is_management


@is_management
def list_all_contracts(user: User, callback=None):
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
    if callback:
        callback()
