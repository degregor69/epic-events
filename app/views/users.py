from getpass import getpass

from app.config import get_db
from app.controllers.users import login_user
from app.views.contracts import list_all_contracts


def login_view():
    email = input("Email: ")
    password = getpass("Password: ")
    db = next(get_db())
    success, message, user = login_user(db, email, password)
    if not success and not user:
        print(f"❌ {message}")
        login_view()

    print(f"✅ {message}")
    role = user.role.name
    print(f"\n👤 Connecté en tant que {user.email} ({role})")

    show_menu(user)


def show_menu(user):
    user_role_name = user.role.name

    if user_role_name == "management":
        print("1. Créer un utilisateur")
        print("2. Voir les contrats")
        print("3. Déconnexion")
        choice = input("Choisissez une option : ")
        if choice == "1":
            pass
        elif choice == "2":
            list_all_contracts(callback=lambda: show_menu(user))
        elif choice == "3":
            print("🔒 Déconnexion...")
        else:
            print("⚠ Option invalide")

    elif user_role_name == "support":
        print("1. Voir mes événements")
        print("2. Déconnexion")
        choice = input("Choisissez une option : ")
        if choice == "1":
            pass
        elif choice == "2":
            print("🔒 Déconnexion...")
        else:
            print("⚠ Option invalide")

    elif user_role_name == "sales":
        print("1. Créer un client")
        print("2. Créer un contrat")
        print("3. Déconnexion")
        choice = input("Choisissez une option : ")
        if choice == "1":
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            print("🔒 Déconnexion...")
        else:
            print("⚠ Option invalide")

    else:
        print("⚠ Aucun menu défini pour ce rôle")
