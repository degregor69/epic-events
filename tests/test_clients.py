from app.controllers.clients import get_all_clients


def test_get_all_clients(db, clients):
    db_clients = get_all_clients(db)

    assert len(db_clients) == len(clients)
