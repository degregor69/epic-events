from datetime import datetime, timedelta

import pytest
from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user
from app.models import Event, Client, Contract, Role


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def roles(db):
    role_names = ["management", "sales", "support"]
    for name in role_names:
        if not db.query(Role).filter_by(name=name).first():
            db.add(Role(name=name))
    db.commit()
    return db.query(Role).filter(Role.name.in_(role_names)).all()


@pytest.fixture
def user(db, roles):
    selected_role = roles[0]
    user = create_user(
        db=db,
        name="Alice Dupont",
        email="alice@example.com",
        password="MotDePasse123!",
        employee_number=1,
        role_id=selected_role.id,
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
def contracts(db, user, clients):
    contract1 = Contract(
        client_id=clients[0].id,
        user_id=user.id,
        total_amount=1000.0,
        pending_amount=500.0,
        signed=True,
    )
    contract2 = Contract(
        client_id=clients[1].id,
        user_id=user.id,
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
def events(db, user, contracts, clients):
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
