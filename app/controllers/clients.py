from sqlalchemy.orm import Session

from app.models import Client, User
from app.utils.permissions import is_sales


def get_all_clients(db: Session):
    return db.query(Client).all()


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
