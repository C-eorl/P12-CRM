from decimal import Decimal

import pytest

from entyties_fixtures import user_commercial, contrat
from src.domain.entities.entities import Contrat

from src.domain.entities.enums import ContractStatus
from src.domain.entities.exceptions import BusinessRuleViolation
from src.domain.entities.value_objects import Money



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

def test_can_be_updated_by(contrat, user_commercial):
    assert contrat.can_be_updated_by(user_commercial) is True