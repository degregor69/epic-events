from app.config import Base, engine
from app.models import User, Client, Contract, Event

if __name__ == "__main__":
    print("📦 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Done!")
