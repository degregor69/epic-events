from sqlalchemy.orm import Session

from app.models import Client, User
from app.utils.permissions import is_sales


def get_all_clients(db: Session):
    return db.query(Client).all()


def get_clients_by_user(db: Session, user_id: int):
    return db.query(Client).filter_by(internal_contact_id=user_id).all()


@is_sales
def create_client(
    db: Session,
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
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@is_sales
def update_client(
    current_user: User,
    db: Session,
    client_id: int,
    full_name: str = None,
    email: str = None,
    phone: str = None,
    company: str = None,
    internal_contact_id: int = None,
):
    client = (
        db.query(Client)
        .filter_by(id=client_id, internal_contact_id=current_user.id)
        .first()
    )
    if not client:
        raise Exception(f"❌ Client with id {client_id} not found")

    if full_name is not None:
        client.full_name = full_name
    if email is not None:
        client.email = email
    if phone is not None:
        client.phone = phone
    if company is not None:
        client.company = company
    if internal_contact_id is not None:
        client.internal_contact_id = internal_contact_id

    db.commit()
    db.refresh(client)
    return client
