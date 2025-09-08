from getpass import getpass

from app.config import get_db
from app.controllers.users import login_user


def login_view():
    email = input("Email: ")
    password = getpass("Password: ")
    db = next(get_db())
    success, message, user = login_user(db, email, password)
    print("✅" if success else "❌", message)

    if not user and not success:
        login_view()

    show_menu(user)


def show_menu(user):
    role = user.role.name
    print(f"👤 Connecté en tant que {user.email} ({role})")

    if role == "management":
        print("\n1. Créer un utilisateur")
        print("2. Voir les contrats")
        print("3. Déconnexion")
    elif role == "support":
        print("\n1. Voir mes événements")
        print("2. Déconnexion")
    elif role == "sales":
        print("\n1. Créer un client")
        print("2. Créer un contrat")
        print("3. Déconnexion")
    else:
        print("⚠ Aucun menu défini pour ce rôle")
