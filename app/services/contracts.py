from sqlalchemy.orm import Session
from app.models import Contract, User
from app.utils.permissions import (
    is_management,
    is_management_or_responsible_sales,
    is_sales,
)
from app.databases.contracts import ContractDB


class ContractService:
    def __init__(self, db: Session):
        self.contract_db = ContractDB(db)

    def get_all_contracts(self):
        return self.contract_db.get_all()

    def get_all_contracts_for_user_clients(self, user_id: int):
        return self.contract_db.get_all_for_clients_user(user_id)

    @is_management
    def create_contract(
        self,
        current_user: User,
        user_id: int,
        client_id: int,
        total_amount: float,
        pending_amount: float,
        signed: bool = False,
    ):
        contract = Contract(
            client_id=client_id,
            user_id=user_id,
            total_amount=total_amount,
            pending_amount=pending_amount,
            signed=signed,
        )
        return self.contract_db.add(contract)

    @is_management_or_responsible_sales
    def update_contract(
        self,
        current_user: User,
        contract_id: int,
        total_amount: float = None,
        pending_amount: float = None,
        signed: bool = None,
        user_id: int = None,
        client_id: int = None,
    ):
        contract = self.contract_db.get_by_id(contract_id)
        if not contract:
            raise Exception(f"Contract with id {contract_id} not found")

        data = {
            "total_amount": total_amount,
            "pending_amount": pending_amount,
            "signed": signed,
            "user_id": user_id,
            "client_id": client_id,
        }
        return self.contract_db.update(contract, data)

    @is_sales
    def get_contracts_filtered(
        self,
        current_user: User,
        only_unsigned: bool = False,
        only_pending: bool = False,
    ):
        return self.contract_db.get_filtered_by_user(
            current_user.id, only_unsigned, only_pending
        )
