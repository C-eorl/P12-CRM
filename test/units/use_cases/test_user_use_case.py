from src.domain.entities.entities import User
from src.domain.entities.value_objects import Email
from src.infrastructures.security.security import BcryptPasswordHasher
from src.use_cases.user_use_cases import CreateUserUseCase, CreateUserRequest, CreateUserResponse, UpdateUserUseCase, \
    UpdateUserRequest, UpdateUserResponse, ListUserUseCase, ListUserResponse, GetUserRequest, GetUserUseCase, \
    GetUserResponse, DeleteUserResponse, DeleteUserRequest, DeleteUserUseCase


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
        role='COMMERCIAL',
        current_user= user_gestion
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
        current_user=user_gestion
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
    repo = user_repository
    user_list_UC = ListUserUseCase(repo)
    response = user_list_UC.execute()

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

    init_count_user = len(repo.find_all())

    request = DeleteUserRequest(
        user_id=2,
        current_user=user_gestion
    )
    response = user_delete_UC.execute(request)

    assert isinstance(response, DeleteUserResponse)
    assert response.success is True
    current_count_user = len(repo.find_all())
    assert current_count_user == init_count_user - 1