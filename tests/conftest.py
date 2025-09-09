from datetime import datetime, timedelta

import pytest
from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user
from app.models import Event, Client, Contract, Role


@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def roles(db):
    role_names = ["management", "sales", "support"]
    roles = []

    for name in role_names:
        role = db.query(Role).filter_by(name=name).first()
        if not role:
            role = Role(name=name)
            db.add(role)
            db.commit()
            db.refresh(role)
        roles.append(role)

    return roles


@pytest.fixture
def support_user(db, roles):
    support_role = next(role for role in roles if role.name == "support")
    user = create_user(
        db=db,
        name="Support User",
        email="support_user@example.com",
        password="MotDePasse123!",
        employee_number=1,
        role_id=support_role.id,
    )
    return user


@pytest.fixture
def management_user(db, roles):
    management_role = next(role for role in roles if role.name == "management")
    user = create_user(
        db=db,
        name="Management User",
        email="management_user@example.com",
        password="MotDePasse123!",
        employee_number=2,
        role_id=management_role.id,
    )
    return user


@pytest.fixture
def sales_user(db, roles):
    sales_role = next(role for role in roles if role.name == "sales")
    user = create_user(
        db=db,
        name="Sales User",
        email="sales_user@example.com",
        password="MotDePasse123!",
        employee_number=3,
        role_id=sales_role.id,
    )
    return user


@pytest.fixture
def clients(db):
    client1 = Client(
        full_name="Client One",
        email="client1@example.com",
        phone="1234567890",
        company="Company A",
        internal_contact="Alice",
    )
    client2 = Client(
        full_name="Client Two",
        email="client2@example.com",
        phone="0987654321",
        company="Company B",
        internal_contact="Bob",
    )
    db.add_all([client1, client2])
    db.commit()
    db.refresh(client1)
    db.refresh(client2)
    return [client1, client2]


@pytest.fixture
def contracts(db, sales_user, clients):
    contract1 = Contract(
        client_id=clients[0].id,
        user_id=sales_user.id,
        total_amount=1000.0,
        pending_amount=500.0,
        signed=True,
    )
    contract2 = Contract(
        client_id=clients[1].id,
        user_id=sales_user.id,
        total_amount=2000.0,
        pending_amount=2000.0,
        signed=False,
    )
    db.add_all([contract1, contract2])
    db.commit()
    db.refresh(contract1)
    db.refresh(contract2)
    return [contract1, contract2]


@pytest.fixture
def events(db, sales_user, contracts, clients):
    now = datetime.now()
    event1 = Event(
        client_id=clients[0].id,
        contract_id=contracts[0].id,
        start_date=now,
        end_date=now + timedelta(hours=2),
        support_contact="Alice",
        location="Brasil",
        attendees=50,
        notes="Need to pay second half of the bill",
    )
    event2 = Event(
        client_id=clients[0].id,
        contract_id=contracts[0].id,
        start_date=now,
        end_date=now + timedelta(hours=2),
        support_contact="Alice",
        location="Montenegro",
        attendees=25,
        notes="Vegetarian event",
    )
    db.add_all([event1, event2])
    db.commit()
    db.refresh(event1)
    db.refresh(event2)
    return [event1, event2]
