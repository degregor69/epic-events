from app.views.users import login_view


def main_view():
    print("🎉 Bienvenue dans Epic Events !")
    print("Veuillez vous connecter pour continuer.\n")
    login_view()
