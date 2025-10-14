from sqlalchemy.orm import Session
from app.models import Client, User, Contract
from app.utils.permissions import is_sales
from app.databases.clients import ClientDB


class ClientService:
    def __init__(self, db: Session):
        self.client_db = ClientDB(db)

    def get_all_clients(self):
        return self.client_db.get_all()

    def get_clients_by_user(self, user_id: int):
        return self.client_db.get_by_user(user_id)

    def get_clients_with_signed_contracts(self, user_id: int):
        return self.client_db.get_clients_with_signed_contrats(user_id)

    @is_sales
    def create_client(
        self,
        current_user: User,
        full_name: str,
        email: str,
        phone: str,
        company: str,
    ):
        client = Client(
            full_name=full_name,
            email=email,
            phone=phone,
            company=company,
            internal_contact_id=current_user.id,
        )
        return self.client_db.add(client)

    @is_sales
    def update_client(
        self,
        current_user: User,
        client_id: int,
        full_name: str = None,
        email: str = None,
        phone: str = None,
        company: str = None,
        internal_contact_id: int = None,
    ):
        client = self.client_db.get_by_id_and_user(client_id, current_user.id)
        if not client:
            raise Exception(f"Client with id {client_id} not found")

        data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "company": company,
            "internal_contact_id": internal_contact_id,
        }
        return self.client_db.update(client, data)
