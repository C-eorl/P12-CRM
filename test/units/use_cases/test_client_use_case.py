import pytest

from src.domain.entities.entities import Client
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy
from src.use_cases.client_use_cases import CreateClientUseCase, CreateClientRequest, CreateClientResponse, \
    GetClientUseCase, UpdateClientUseCase, UpdateClientRequest, UpdateClientResponse, ListClientUseCase, \
    ListClientResponse, GetClientRequest, GetClientResponse, DeleteClientUseCase, DeleteClientRequest, \
    DeleteClientResponse, ListClientRequest


######################################################################
#                            Create Client Use Case                  #
######################################################################
def test_create_client (client_repository):
    """Test creating a new client via use case"""
    repo = client_repository
    client_create_UC = CreateClientUseCase(repo)
    request = CreateClientRequest(
        fullname="test",
        email="test@mail.fr",
        telephone="0245568754",
        company_name="test company",
        authorization= RequestPolicy(
                        user={"user_current_id": 1, "user_current_role": Role.COMMERCIAL},
                        ressource="CLIENT",
                        action="create",
                    )
    )

    response = client_create_UC.execute(request)

    assert isinstance(response, CreateClientResponse)
    assert response.success is True
    assert isinstance(response.client, Client)
    found_client = repo.find_by_id(3)
    assert response.client.id == found_client.id

def test_create_no_commercial_user(client_repository):
    """Test creating a new client via use case with no commercial user"""
    repo = client_repository
    client_create_UC = CreateClientUseCase(repo)
    request = CreateClientRequest(
        fullname="test",
        email="test@mail.fr",
        telephone="0245568754",
        company_name="test company",
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.GESTION},
            ressource="CLIENT",
            action="create",
        )
    )

    response = client_create_UC.execute(request)

    assert isinstance(response, CreateClientResponse)
    assert response.success is False

def test_create_invalid_data(client_repository):
    """Test creating a new client via use case with invalid data"""
    repo = client_repository
    client_create_UC = CreateClientUseCase(repo)
    request = CreateClientRequest(
        fullname="test",
        email="test@",
        telephone="02454",
        company_name="test company",
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.COMMERCIAL},
            ressource="CLIENT",
            action="create",
        )
    )

    response = client_create_UC.execute(request)

    assert isinstance(response, CreateClientResponse)
    assert response.success is False

######################################################################
#                            Update Client Use Case                  #
######################################################################

def test_update_client(client_repository):
    """Test updated a client via use case"""
    repo = client_repository
    client_update_UC = UpdateClientUseCase(repo)
    request = UpdateClientRequest(
        client_id=1,
        fullname="modified fullname",
        email=None,
        telephone=None,
        company_name=None,
        authorization=RequestPolicy(
            user={"user_current_id": 3, "user_current_role": Role.COMMERCIAL},
            ressource="CLIENT",
            action="update",
        )
    )

    response = client_update_UC.execute(request)

    assert isinstance(response, UpdateClientResponse)
    assert response.success is True
    assert isinstance(response.client, Client)
    found_client = repo.find_by_id(1)
    assert found_client.fullname == "modified fullname"

def test_update_client_invalid_data(client_repository):
    """Test update a client via use case with invalid data"""
    repo = client_repository
    client_update_UC = UpdateClientUseCase(repo)
    request = UpdateClientRequest(
        client_id=1,
        fullname=None,
        email="invalid",
        telephone=None,
        company_name=None,
        authorization=RequestPolicy(
            user={"user_current_id": 3, "user_current_role": Role.COMMERCIAL},
            ressource="CLIENT",
            action="update",
        )
    )

    response = client_update_UC.execute(request)

    assert isinstance(response, UpdateClientResponse)
    assert response.success is False

def test_update_client_no_commercial(user_gestion, client_repository):
    """Test update a client via use case with no commercial user"""
    repo = client_repository
    client_update_UC = UpdateClientUseCase(repo)
    request = UpdateClientRequest(
        client_id=1,
        fullname=None,
        email="invalid",
        telephone=None,
        company_name=None,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.GESTION},
            ressource="CLIENT",
            action="update",
        )
    )

    response = client_update_UC.execute(request)

    assert isinstance(response, UpdateClientResponse)
    assert response.success is False

def test_update_client_no_associe_commercial(user_commercial2, client_repository):
    """Test update a client via use case with no commercial user"""
    repo = client_repository
    client_update_UC = UpdateClientUseCase(repo)
    request = UpdateClientRequest(
        client_id=1,
        fullname=None,
        email="invalid",
        telephone=None,
        company_name=None,
        authorization=RequestPolicy(
            user={"user_current_id": 25, "user_current_role": Role.COMMERCIAL},
            ressource="CLIENT",
            action="update",
        )
    )

    response = client_update_UC.execute(request)

    assert isinstance(response, UpdateClientResponse)
    assert response.success is False

######################################################################
#                            Get List Client Use Case                #
######################################################################

def test_get_list_client(user_commercial, client_repository):
    """Test get client list via use case (2 clients saved)"""
    request = ListClientRequest(
        user_id=3,
        list_filter=None
    )

    repo = client_repository
    client_list_UC = ListClientUseCase(repo)
    response = client_list_UC.execute(request)

    assert isinstance(response, ListClientResponse)
    assert response.success is True
    assert isinstance(response.clients, list)

######################################################################
#                            Get by id Client Use Case                  #
######################################################################

def test_get_client_by_id(user_commercial, client_repository):
    """Test getting a client by id via use case"""
    repo = client_repository
    client_get_UC = GetClientUseCase(repo)
    request = GetClientRequest(
        client_id=1,
    )
    response = client_get_UC.execute(request)

    assert isinstance(response, GetClientResponse)
    assert response.success is True
    assert isinstance(response.client, Client)

def test_get_client_by_invalid_id(user_commercial, client_repository):
    """Test getting a client by invalid id via use case"""
    repo = client_repository
    client_get_UC = GetClientUseCase(repo)
    request = GetClientRequest(
        client_id=456,
    )
    response = client_get_UC.execute(request)

    assert isinstance(response, GetClientResponse)
    assert response.success is False

######################################################################
#                            Delete Client Use Case                  #
######################################################################

def test_delete_client_no_admin(user_commercial, client_repository):
    """Test deleting a client via use case  (2 client saved) """
    user_commercial.id = 3
    repo = client_repository
    client_delete_UC = DeleteClientUseCase(repo)
    request = DeleteClientRequest(
        client_id=1,
        authorization=RequestPolicy(
            user={"user_current_id": 2, "user_current_role": Role.COMMERCIAL},
            ressource="CLIENT",
            action="delete",

        )
    )
    response = client_delete_UC.execute(request)
    print(repo.find_by_id(1))

    assert isinstance(response, DeleteClientResponse)
    assert response.success is False

