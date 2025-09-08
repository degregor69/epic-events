from app.utils.auth import is_authenticated
from app.controllers.clients import get_all_clients
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
