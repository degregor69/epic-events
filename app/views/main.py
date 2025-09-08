from app.views.users import login_view


def main_view():
    print("🎉 Bienvenue dans Epic Events !")
    print("Veuillez vous connecter pour continuer.\n")
    login_view()


def show_menu(user):
    role = user.role.name
    print(f"\n👤 Connecté en tant que {user.email} ({role})")

    if role == "management":
        print("1. Créer un utilisateur")
        print("2. Voir les contrats")
        print("3. Déconnexion")
    elif role == "support":
        print("1. Voir mes événements")
        print("2. Déconnexion")
    elif role == "sales":
        print("1. Créer un client")
        print("2. Créer un contrat")
        print("3. Déconnexion")
    else:
        print("⚠ Aucun menu défini pour ce rôle")
