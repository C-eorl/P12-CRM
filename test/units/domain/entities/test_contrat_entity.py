from decimal import Decimal

import pytest

from src.domain.entities.entities import Contrat, Client, User
from src.domain.entities.enums import ContractStatus, Role
from src.domain.entities.exceptions import BusinessRuleViolation
from src.domain.entities.value_objects import Email, Telephone, Money


@pytest.fixture
def user():
    return User(id=1, full_name="test test",
                email=Email("test@test.com"), password="sfsefs",
                role=Role.COMMERCIAL)

@pytest.fixture
def client():
    return Client(
        id=5,
        fullname="test test",
        email=Email("mail@test.com"),
        telephone=Telephone("0245785689"),
        company_name="test",
        commercial_contact= 1
    )

@pytest.fixture(scope="function")
def contrat():
    return Contrat(
        id=1,
        client= 5,
        commercial_contact= 1,
        contrat_amount=Money(100),
        balance_due=Money(100),
        status= ContractStatus.UNSIGNED
    )


def test_contrat_entity(contrat):
    assert isinstance(contrat, Contrat)

def test_contrat_already_signed(contrat):
    contrat.sign()
    with pytest.raises(BusinessRuleViolation):
        contrat.sign()

def test_contrat_sign(contrat):
    contrat.sign()
    assert contrat.status == ContractStatus.SIGNED

def test_contrat_record_payment(contrat):
    payment = Money(50)
    contrat.record_payment(payment)
    assert contrat.balance_due == Money(50)

def test_contrat_record_overpayment(contrat):
    with pytest.raises(BusinessRuleViolation):
        payment = Money(150)
        contrat.record_payment(payment)

def test_contrat_is_fully_paid(contrat):
    contrat.record_payment(Money(100))
    assert contrat.is_fully_paid() is True

def test_contrat_is_not_fully_paid(contrat):
    contrat.record_payment(Money(10))
    assert contrat.is_fully_paid() is False

def test_can_be_updated_by(contrat, user):
    assert contrat.can_be_updated_by(user) is True