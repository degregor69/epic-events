import pytest
from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user
from app.models import User


# Fixture pour créer les tables et fournir une session
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    user = create_user(
        db=db,  # on passe la session
        name="Alice Dupont",
        email="alice@example.com",
        password="MotDePasse123!",
        team="management",
        employee_number=1,
    )
    assert user.id is not None

    db_user = db.query(User).filter_by(email="alice@example.com").first()
    assert db_user is not None
    assert db_user.hashed_password != "MotDePasse123!"
