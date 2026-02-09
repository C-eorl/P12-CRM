from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email
from src.domain.policies.user_policy import RequestPolicy
from src.infrastructures.security.security import BcryptPasswordHasher
from src.use_cases.user_use_cases import CreateUserUseCase, CreateUserRequest, CreateUserResponse, UpdateUserUseCase, \
    UpdateUserRequest, UpdateUserResponse, ListUserUseCase, ListUserResponse, GetUserRequest, GetUserUseCase, \
    GetUserResponse, DeleteUserResponse, DeleteUserRequest, DeleteUserUseCase, ListUserRequest


######################################################################
#                            Create User Use Case                  #
######################################################################
def test_create_user(user_repository, user_gestion):
    repo = user_repository
    hash_password = BcryptPasswordHasher()
    user_create_UC = CreateUserUseCase(repo, hash_password)
    request = CreateUserRequest(
        fullname='test',
        email='test@test.fr',
        password='testtest',
        role=Role.COMMERCIAL,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="USER",
            action="create",
        )
    )

    response = user_create_UC.execute(request)

    assert isinstance(response, CreateUserResponse)
    assert response.success is True
    assert isinstance(response.user, User)
    found_user = repo.find_by_id(4)
    assert response.user.id == found_user.id

######################################################################
#                            Update User Use Case                  #
######################################################################
def test_update_user(user_repository, user_gestion):
    repo = user_repository
    user_update_UC = UpdateUserUseCase(repo)
    request = UpdateUserRequest(
        user_id = 1,
        fullname='test_modify henri',
        email="modify.email@mail.fr",
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="USER",
            action="create",
        )
    )
    response = user_update_UC.execute(request)

    assert isinstance(response, UpdateUserResponse)
    assert response.success is True
    assert isinstance(response.user, User)
    found_user = repo.find_by_id(1)
    assert found_user.fullname == 'test_modify henri'
    assert found_user.email == Email("modify.email@mail.fr")

######################################################################
#                            Get List User Use Case                #
######################################################################
def test_get_list_user(user_repository):
    """Test get users list via use case (3 users saved)"""
    request = ListUserRequest(
        list_filter=None
    )

    repo = user_repository
    user_list_UC = ListUserUseCase(repo)
    response = user_list_UC.execute(request)

    assert isinstance(response, ListUserResponse)
    assert response.success is True
    assert isinstance(response.users, list)
    assert len(response.users) == 3

######################################################################
#                            Get by id User Use Case                 #
######################################################################

def test_get_user_by_id(user_repository):
    """Test getting a user by id via use case"""
    repo = user_repository
    user_get_UC = GetUserUseCase(repo)
    request = GetUserRequest(
        user_id=2,
    )
    response = user_get_UC.execute(request)

    assert isinstance(response, GetUserResponse)
    assert response.success is True
    assert isinstance(response.user, User)

######################################################################
#                            Delete User Use Case                  #
######################################################################

def test_delete_user(user_repository,user_gestion):
    """Test deleting a client via use case  (3 users saved) """
    repo = user_repository
    user_delete_UC = DeleteUserUseCase(repo)

    user = repo.save(user_gestion)

    request = DeleteUserRequest(
        user_id=user.id,
        authorization=RequestPolicy(
            user={"user_current_id": 1, "user_current_role": Role.GESTION},
            ressource="USER",
            action="create",
        )
    )
    response = user_delete_UC.execute(request)

    assert isinstance(response, DeleteUserResponse)
    assert response.success is True
    assert repo.find_by_id(user.id) is None