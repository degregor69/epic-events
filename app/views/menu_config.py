from app.views.contracts import (
    list_all_contracts,
    create_contract_view,
    update_contract_view,
    list_contracts_filtered_view,
)
from app.views.clients import list_all_clients, create_client_view, update_client_view
from app.views.events import (
    list_all_events,
    list_events_without_support_view,
    update_event_view,
    create_event_view,
    list_my_events,
)
from app.views.users import create_user_view, update_user_view, delete_user_view

common_menu = [
    ("Voir tous les contrats", list_all_contracts),
    ("Voir tous les clients", list_all_clients),
    ("Voir tous les événements", list_all_events),
]

role_specific = {
    "management": [
        ("Créer un utilisateur", create_user_view),
        ("Modifier un utilisateur", update_user_view),
        ("Supprimer un utilisateur", delete_user_view),
        ("Créer un contrat", create_contract_view),
        ("Modifier un contrat", update_contract_view),
        ("Voir les événements sans support", list_events_without_support_view),
        ("Modifier un événement", update_event_view),
    ],
    "sales": [
        ("Créer un client", create_client_view),
        ("Modifier un client", update_client_view),
        ("Modifier un contrat", update_contract_view),
        ("Voir mes contrats", list_contracts_filtered_view),
        ("Créer un événement", create_event_view),
    ],
    "support": [
        ("Voir mes événements", list_my_events),
        ("Modifier mes événements", update_event_view),
    ],
}

logout_option = [("Déconnexion", None)]
