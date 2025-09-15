import pytest

from app.controllers.contracts import get_all_contracts, create_contract
from app.models import Contract


def test_get_all_contracts(db, contracts):
    db_contracts = get_all_contracts(db)

    assert len(db_contracts) == len(contracts)


def test_create_contract(db, management_user, contracts, clients):
    created_contract = create_contract(
        current_user=management_user,
        db=db,
        user_id=management_user.id,
        client_id=clients[0].id,
        total_amount=5000,
        pending_amount=2000,
        signed=True,
    )

    assert created_contract is not None

    db_created_contract: Contract = db.get(Contract, created_contract.id)

    assert db_created_contract.id == created_contract.id
    assert db_created_contract.user_id == management_user.id
    assert db_created_contract.client_id == clients[0].id
    assert db_created_contract.total_amount == 5000
    assert db_created_contract.pending_amount == 2000
    assert db_created_contract.signed is True


def test_create_contract_with_non_authorized_user(
    db, support_user, management_user, contracts, clients
):
    with pytest.raises(Exception) as exc:
        create_contract(support_user)
        assert str(exc.value) == "Accès refusé (réservé au Management)"
