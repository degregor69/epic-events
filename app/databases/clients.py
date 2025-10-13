from sqlalchemy.orm import Session
from app.models import Client
from app.models.contracts import Contract


class ClientDB:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Client).all()

    def get_by_user(self, user_id: int):
        return self.db.query(Client).filter_by(internal_contact_id=user_id).all()

    def get_by_id_and_user(self, client_id: int, user_id: int):
        return (
            self.db.query(Client)
            .filter_by(id=client_id, internal_contact_id=user_id)
            .first()
        )

    def get_clients_with_signed_contrats(self, user_id: int):
        clients = (
            self.db.query(Client)
            .join(Contract, Contract.client_id == Client.id)
            .filter(Client.internal_contact_id == user_id)
            .filter(Contract.signed.is_(True))
            .all()
        )
        return clients

    def add(self, client: Client):
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def update(self, client: Client, data: dict):
        for field, value in data.items():
            if hasattr(client, field) and value is not None:
                setattr(client, field, value)
        self.db.commit()
        self.db.refresh(client)
        return client
