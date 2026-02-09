from src.domain.entities.entities import Contrat
from src.domain.entities.enums import Role, ContractStatus
from src.domain.entities.value_objects import Money
from src.domain.policies.user_policy import RequestPolicy
from src.use_cases.contrat_use_cases import ListContratUseCase, ListContratResponse, ListContratRequest
from src.use_cases.contrat_use_cases import GetContratUseCase, GetContratRequest, GetContratResponse
from src.use_cases.contrat_use_cases import (
    DeleteContratUseCase,
    DeleteContratRequest,
    DeleteContratResponse,
)
from src.use_cases.contrat_use_cases import (
    UpdateContratUseCase,
    UpdateContratRequest,
    UpdateContratResponse,
)

from src.use_cases.contrat_use_cases import (
    CreateContratUseCase,
    CreateContratRequest,
    CreateContratResponse,
)
from src.use_cases.contrat_use_cases import (
    SignContratUseCase,
    SignContratRequest,
    SignContratResponse,
)
from src.use_cases.contrat_use_cases import (
    RecordPaymentContratUseCase,
    RecordPaymentContratRequest,
    RecordPaymentContratResponse,
)

######################################################################
#                            Create Contrat Use Case                 #
######################################################################
def test_create_contrat(contrat_repository):
    """Test creating a new contrat via use case"""
    repo = contrat_repository
    uc = CreateContratUseCase(repo)

    request = CreateContratRequest(
        client_id=1,
        commercial_contact_id=3,
        contrat_amount=Money(1000),
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="create",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, CreateContratResponse)
    assert response.success is True
    assert isinstance(response.contrat, Contrat)

    found = repo.find_by_id(response.contrat.id)
    assert found is not None
    assert found.status == ContractStatus.UNSIGNED

def test_create_contrat_no_gestion_user(contrat_repository):
    """Test creating a contrat without gestion permission"""
    repo = contrat_repository
    uc = CreateContratUseCase(repo)

    request = CreateContratRequest(
        client_id=1,
        commercial_contact_id=3,
        contrat_amount=Money(1000),
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.COMMERCIAL},
            ressource="CONTRAT",
            action="create",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, CreateContratResponse)
    assert response.success is False
    assert response.contrat is None

######################################################################
#                            Update Contrat Use Case                 #
######################################################################
def test_update_contrat(contrat_repository):
    """Test updating a contrat via use case"""
    repo = contrat_repository
    uc = UpdateContratUseCase(repo)

    request = UpdateContratRequest(
        contrat_id=1,
        contrat_amount=Money(2000),
        status=ContractStatus.SIGNED,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="update",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, UpdateContratResponse)
    assert response.success is True

    updated = repo.find_by_id(1)
    assert updated.contrat_amount.amount == 2000
    assert updated.status == ContractStatus.SIGNED

def test_update_contrat_not_found(contrat_repository):
    """Test updating a non-existing contrat"""
    repo = contrat_repository
    uc = UpdateContratUseCase(repo)

    request = UpdateContratRequest(
        contrat_id=999,
        contrat_amount=Money(1000),
        status=None,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="update",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, UpdateContratResponse)
    assert response.success is False

def test_update_contrat_no_permission(contrat_repository):
    """Test updating a contrat without permission"""
    repo = contrat_repository
    uc = UpdateContratUseCase(repo)

    request = UpdateContratRequest(
        contrat_id=1,
        contrat_amount=Money(1500),
        status=None,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.COMMERCIAL},
            ressource="CONTRAT",
            action="update",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, UpdateContratResponse)
    assert response.success is False

######################################################################
#                            List Contrat Use Case                   #
######################################################################
def test_list_contrat(contrat_repository):
    """Test listing contrats"""
    request = ListContratRequest(
        commercial_contact_id=3,
        list_filter=None
    )

    repo = contrat_repository
    uc = ListContratUseCase(repo)

    response = uc.execute(request)

    assert isinstance(response, ListContratResponse)
    assert response.success is True
    assert isinstance(response.contrats, list)

######################################################################
#                            Get Contrat Use Case                   #
######################################################################
def test_get_contrat_by_id(contrat_repository):
    """Test get contrat by id"""
    repo = contrat_repository
    uc = GetContratUseCase(repo)

    request = GetContratRequest(contrat_id=1)
    response = uc.execute(request)

    assert isinstance(response, GetContratResponse)
    assert response.success is True
    assert isinstance(response.contrat, Contrat)

def test_get_contrat_invalid_id(contrat_repository):
    """Test get contrat with invalid id"""
    repo = contrat_repository
    uc = GetContratUseCase(repo)

    request = GetContratRequest(contrat_id=999)
    response = uc.execute(request)

    assert isinstance(response, GetContratResponse)
    assert response.success is False

######################################################################
#                            Delete Contrat Use Case                 #
######################################################################
def test_delete_contrat_admin(contrat_repository):
    """Test deleting a contrat as admin"""
    repo = contrat_repository
    uc = DeleteContratUseCase(repo)

    request = DeleteContratRequest(
        contrat_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.ADMIN},
            ressource="CONTRAT",
            action="delete",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, DeleteContratResponse)
    assert response.success is True
    assert repo.find_by_id(1) is None

def test_delete_contrat_no_admin(contrat_repository):
    """Test deleting a contrat without admin role"""
    repo = contrat_repository
    uc = DeleteContratUseCase(repo)

    request = DeleteContratRequest(
        contrat_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="delete",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, DeleteContratResponse)
    assert response.success is False

######################################################################
#                            Sign Contrat Use Case                 #
######################################################################
def test_sign_contrat_success(contrat_repository):
    """Test signing a contrat"""
    repo = contrat_repository
    contrat_db = repo.find_by_id(1)
    contrat_db.commercial_contact_id = 1
    uc = SignContratUseCase(repo)

    request = SignContratRequest(
        contrat_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.COMMERCIAL},
            ressource="CONTRAT",
            action="sign",
            context=contrat_db,
        )
    )

    response = uc.execute(request)

    assert isinstance(response, SignContratResponse)
    assert response.success is True
    assert isinstance(response.contrat, Contrat)
    assert response.contrat.status == ContractStatus.SIGNED

def test_sign_contrat_not_found(contrat_repository):
    """Test signing a non-existing contrat"""
    repo = contrat_repository
    uc = SignContratUseCase(repo)

    request = SignContratRequest(
        contrat_id=999,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="sign",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, SignContratResponse)
    assert response.success is False
    assert response.contrat is None

def test_sign_contrat_no_permission(contrat_repository):
    """Test signing a contrat without permission"""
    repo = contrat_repository
    uc = SignContratUseCase(repo)

    request = SignContratRequest(
        contrat_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.COMMERCIAL},
            ressource="CONTRAT",
            action="sign",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, SignContratResponse)
    assert response.success is False

def test_sign_contrat_already_signed(contrat_repository):
    """Test signing an already signed contrat"""
    repo = contrat_repository
    contrat_db = repo.find_by_id(1)
    contrat_db.status = ContractStatus.SIGNED
    repo.save(contrat_db)

    uc = SignContratUseCase(repo)

    request = SignContratRequest(
        contrat_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="sign",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, SignContratResponse)
    assert response.success is False

######################################################################
#                            Pay Contrat Use Case                    #
######################################################################
def test_record_payment_success(contrat_repository):
    """Test recording a payment on a contrat"""
    repo = contrat_repository
    contrat_db = repo.find_by_id(1)
    contrat_db.commercial_contact_id = 1
    uc = RecordPaymentContratUseCase(repo)

    request = RecordPaymentContratRequest(
        contrat_id=1,
        payment=5,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.COMMERCIAL},
            ressource="CONTRAT",
            action="pay",
            context=contrat_db
        )
    )

    response = uc.execute(request)

    assert isinstance(response, RecordPaymentContratResponse)
    assert response.success is True
    assert response.contrat.balance_due.amount < response.contrat.contrat_amount.amount

def test_record_payment_contrat_not_found(contrat_repository):
    """Test recording payment on non-existing contrat"""
    repo = contrat_repository
    uc = RecordPaymentContratUseCase(repo)

    request = RecordPaymentContratRequest(
        contrat_id=999,
        payment=100,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="pay",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, RecordPaymentContratResponse)
    assert response.success is False

def test_record_payment_no_permission(contrat_repository):
    """Test recording payment without permission"""
    repo = contrat_repository
    uc = RecordPaymentContratUseCase(repo)

    request = RecordPaymentContratRequest(
        contrat_id=1,
        payment=100,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.COMMERCIAL},
            ressource="CONTRAT",
            action="pay",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, RecordPaymentContratResponse)
    assert response.success is False

def test_record_payment_fully_paid_contrat(contrat_repository):
    """Test payment on fully paid contrat"""
    repo = contrat_repository
    contrat_db = repo.find_by_id(1)

    contrat_db.record_payment(contrat_db.balance_due)
    repo.save(contrat_db)

    uc = RecordPaymentContratUseCase(repo)

    request = RecordPaymentContratRequest(
        contrat_id=1,
        payment=100,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="pay",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, RecordPaymentContratResponse)
    assert response.success is False

def test_record_payment_invalid_amount(contrat_repository):
    """Test invalid payment amount"""
    repo = contrat_repository
    uc = RecordPaymentContratUseCase(repo)

    request = RecordPaymentContratRequest(
        contrat_id=1,
        payment=-100,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="CONTRAT",
            action="pay",
        )
    )

    response = uc.execute(request)

    assert isinstance(response, RecordPaymentContratResponse)
    assert response.success is False

