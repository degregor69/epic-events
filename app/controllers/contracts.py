from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User

from app.models import Contract, Client
from app.utils.permissions import is_management, is_management_or_responsible_sales


def get_all_contracts(db: Session):
    return db.query(Contract).all()


def get_all_contracts_for_clients_user(db: Session, user_id: int):
    return db.query(Contract).join(Client).filter_by(internal_contact_id=user_id).all()


@is_management
def create_contract(
    current_user: User,
    db: Session,
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
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


@is_management_or_responsible_sales
def update_contract(
    current_user: User,
    db: Session,
    contract_id: int,
    total_amount: float = None,
    pending_amount: float = None,
    signed: bool = None,
    user_id: int = None,
    client_id: int = None,
):
    contract = db.query(Contract).filter_by(id=contract_id).first()
    if not contract:
        raise Exception(f"❌ Contract with id {contract_id} not found")

    if total_amount is not None:
        contract.total_amount = total_amount
    if pending_amount is not None:
        contract.pending_amount = pending_amount
    if signed is not None:
        contract.signed = signed
    if user_id is not None:
        contract.user_id = user_id
    if client_id is not None:
        contract.client_id = client_id

    db.commit()
    db.refresh(contract)
    return contract
