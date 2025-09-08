from app.config import Base, engine, SessionLocal
from app.controllers.users import create_user
from app.models import User
from app.models.roles import Role


def seed_roles(db: SessionLocal):
    roles_names = ["management", "commercial", "support"]
    roles = []
    for role_name in roles_names:
        if not db.query(Role).filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.add(role)
            roles.append(role)
    db.commit()
    for role in roles:
        db.refresh(role)
    db.close()
    print("✅ Roles seed created")
    return roles


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    roles = seed_roles(session)

    existing = (
        session.query(User).filter_by(email="test_management@epic-events.com").first()
    )
    if not existing:
        user = create_user(
            db=session,
            name="Test Manager",
            email="test_management@epic-events.com",
            password="test123?",
            role_id=roles[1].id,
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
