import pytest

from app.controllers.contracts import (
    get_all_contracts,
    create_contract,
    update_contract,
)
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


def test_update_contract(db, management_user, contracts, clients):
    contract = contracts[0]

    updated_contract = update_contract(
        current_user=management_user,
        db=db,
        contract_id=contract.id,
        total_amount=7500,
        pending_amount=3500,
        signed=True,
        user_id=management_user.id,
        client_id=clients[1].id,
    )

    assert updated_contract is not None

    db_updated_contract: Contract = db.get(Contract, contract.id)

    assert db_updated_contract.id == contract.id
    assert db_updated_contract.total_amount == 7500
    assert db_updated_contract.pending_amount == 3500
    assert db_updated_contract.signed is True
    assert db_updated_contract.user_id == management_user.id
    assert db_updated_contract.client_id == clients[1].id


def test_update_contract_with_non_authorized_user(
    db, support_user, management_user, contracts, clients
):
    with pytest.raises(Exception) as exc:
        update_contract(support_user)
        assert str(exc.value) == "Accès refusé (réservé au Management)"
