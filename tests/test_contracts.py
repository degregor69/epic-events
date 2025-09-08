from app.controllers.contracts import get_all_contracts


def test_get_all_contracts(db, contracts):
    db_contracts = get_all_contracts(db)

    assert len(db_contracts) == len(contracts)
