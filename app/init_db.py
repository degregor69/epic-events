from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user
from app.models import User


def seed():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    existing = (
        session.query(User).filter_by(email="test_management@epic-events.com").first()
    )
    if not existing:
        user = create_user(
            db=session,
            name="Test Manager",
            email="test_management@epic-events.com",
            password="test123?",
            team="management",
            employee_number=1,
        )
        session.add(user)
        session.commit()
        print("✅ User seed created")
    else:
        print("⚠ User already exists")

    session.close()


if __name__ == "__main__":
    seed()
