from datetime import datetime

from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user
from app.models import User, Client, Contract
from app.models.roles import Role


def seed_roles(db: SessionLocal):
    roles_names = ["management", "sales", "support"]
    roles = []
    for role_name in roles_names:
        if not db.query(Role).filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.add(role)
            roles.append(role)
    db.commit()
    for role in roles:
        db.refresh(role)
    print("✅ Roles seed created")
    return roles


def seed_clients(db: SessionLocal):
    client = db.query(Client).filter_by(email="client@test.com").first()
    if not client:
        client = Client(
            full_name="Test Client",
            email="client@test.com",
            phone="0123456789",
            company="TestCorp",
            internal_contact="Michel Test",
        )
        db.add(client)
        db.commit()
        print("✅ Client created")
    return client


def seed_contracts(db: SessionLocal, client_id: int, user_id: int):
    contract = (
        db.query(Contract).filter_by(client_id=client_id, user_id=user_id).first()
    )
    if not contract:
        contract = Contract(
            client_id=client_id,
            user_id=user_id,
            total_amount=10000,
            pending_amount=5000,
            signed=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(contract)
        db.commit()
        print("✅ Contract created")
    else:
        print("⚠ Contract already exists")


def seed_management_user(db: SessionLocal, role_id: int):
    existing = db.query(User).filter_by(email="test_management@epic-events.com").first()
    if not existing:
        user = create_user(
            db=db,
            name="Test Manager",
            email="test_management@epic-events.com",
            password="test123?",
            role_id=role_id,
            employee_number=1,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    else:
        print("⚠ User already exists")


def seed_sales_user(db: SessionLocal, role_id: int):
    existing = db.query(User).filter_by(email="test_sales@epic-events.com").first()
    if not existing:
        user = create_user(
            db=db,
            name="Test Sales",
            email="test_sales@epic-events.com",
            password="test123?",
            role_id=role_id,
            employee_number=3,
        )
        db.add(user)
        db.commit()


def seed_support_user(db: SessionLocal, role_id: int):
    existing = db.query(User).filter_by(email="test_support@epic-events.com").first()
    if not existing:
        user = create_user(
            db=db,
            name="Test Support",
            email="test_support@epic-events.com",
            password="test123?",
            role_id=role_id,
            employee_number=2,
        )
        db.add(user)
        db.commit()


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    roles = seed_roles(db)
    management_role = next(role for role in roles if role.name == "management")
    support_role = next(role for role in roles if role.name == "support")
    sales_role = next(role for role in roles if role.name == "sales")

    management_user = seed_management_user(db, management_role.id)
    support_user = seed_support_user(db, support_role.id)
    sales_user = seed_sales_user(db, sales_role.id)

    client = seed_clients(db)
    contract = seed_contracts(db, client.id, management_user.id)
    db.close()


if __name__ == "__main__":
    seed()
