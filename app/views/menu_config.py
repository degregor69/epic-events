from app.views.contracts import list_all_contracts
from app.views.clients import list_all_clients
from app.views.events import list_all_events

common_menu = [
    ("Voir tous les contrats", list_all_contracts),
    ("Voir tous les clients", list_all_clients),
    ("Voir tous les événements", list_all_events),
]

role_specific = {
    "management": [("Créer un utilisateur", lambda user: print("TODO: créer user"))],
    "sales": [
        ("Créer un client", lambda user: print("TODO: créer client")),
        ("Créer un contrat", lambda user: print("TODO: créer contrat")),
    ],
    "support": [
        ("Voir mes événements", lambda user: print("TODO: événements support"))
    ],
}

logout_option = [("Déconnexion", lambda user: print("🔒 Déconnexion..."))]
