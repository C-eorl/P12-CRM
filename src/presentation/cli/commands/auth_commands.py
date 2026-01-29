import typer

from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher, JWTTokenManager
from src.use_cases.auth_use_cases import AuthenticateUseCase, AuthenticateRequest

auth_app = typer.Typer()

@auth_app.command()
def login(ctx: typer.Context,
        email: str = typer.Option(prompt=True),
        password: str = typer.Option(prompt=True, hide_input=True)
):
    """Connect user to email & password"""
    # execute use case authenticate
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    password_hasher = BcryptPasswordHasher()
    token_manager = JWTTokenManager()
    use_case = AuthenticateUseCase(repo, password_hasher, token_manager)

    request = AuthenticateRequest(email, password)
    response = use_case.execute(request)
    if response.success is False:
        typer.echo(f"{response.error}")
    else:
        typer.echo("Vous êtes connecté")

