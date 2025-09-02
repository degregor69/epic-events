import pytest
from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def user(db):
    user = create_user(
        db=db,
        name="Alice Dupont",
        email="alice@example.com",
        password="MotDePasse123!",
        team="management",
        employee_number=1,
    )
    return user
