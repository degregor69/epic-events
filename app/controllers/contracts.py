from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User

from app.models import Contract
from app.utils.permissions import is_management


def get_all_contracts(db: Session):
    return db.query(Contract).all()


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
