from app.views.menu_config import common_menu, role_specific, logout_option
from app.views.users import login_view


def main_view():
    print("🎉 Bienvenue dans Epic Events !")
    print("Veuillez vous connecter pour continuer.\n")
    user = login_view()
    if user:
        show_menu(user)


# app/views/menu.py
from app.views.menu_config import common_menu, role_specific, logout_option


def show_menu(user):
    role = user.role.name

    options = common_menu + role_specific.get(role, []) + logout_option

    while True:
        print("\n=== MENU ===")
        for i, (label, _) in enumerate(options, start=1):
            print(f"{i}. {label}")

        choice = input("Choisissez une option : ")

        try:
            index = int(choice) - 1
            label, action = options[index]

            if label == "Déconnexion":
                print("🔒 Déconnexion...")
                break
            action(user)

        except (ValueError, IndexError):
            print("⚠ Option invalide")
