import typer

from src.infrastructures.database.session import get_session
from src.infrastructures.repositories.SQLAchemy_repository import SQLAchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher, JWTTokenManager
from src.use_cases.auth_use_cases import AuthenticateUseCase, AuthenticateRequest

auth_app = typer.Typer()

@auth_app.command()
def login(email: str, password: str):
    """Connect user to email & password"""
    # execute use case authenticate
    session = get_session()
    repo = SQLAchemyUserRepository(session)
    password_hasher = BcryptPasswordHasher()
    token_manager = JWTTokenManager()
    use_case = AuthenticateUseCase(repo, password_hasher, token_manager)

    request = AuthenticateRequest(email, password)
    response = use_case.execute(request)
    if response.success is False:
        typer.echo(f"{response.error}")
    else:
        typer.echo("Vous êtes connecté")

