from sqlalchemy.orm import Session
from app.models import Contract, Client


class ContractDB:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Contract).all()

    def get_all_for_clients_user(self, user_id: int):
        return (
            self.db.query(Contract)
            .join(Client)
            .filter_by(internal_contact_id=user_id)
            .all()
        )

    def get_by_id(self, contract_id: int):
        return self.db.query(Contract).filter_by(id=contract_id).first()

    def add(self, contract: Contract):
        self.db.add(contract)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def update(self, contract: Contract, data: dict):
        for field, value in data.items():
            if hasattr(contract, field) and value is not None:
                setattr(contract, field, value)
        self.db.commit()
        self.db.refresh(contract)
        return contract

    def get_filtered_by_user(
        self, user_id: int, only_unsigned: bool, only_pending: bool
    ):
        query = (
            self.db.query(Contract).join(Client).filter_by(
                internal_contact_id=user_id)
        )
        if only_unsigned:
            query = query.filter(Contract.signed == False)
        if only_pending:
            query = query.filter(Contract.pending_amount > 0)
        return query.all()
