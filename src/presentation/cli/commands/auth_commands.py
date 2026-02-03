import typer
from rich.console import Console

from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher, JWTTokenManager, TokenStore
from src.use_cases.auth_use_cases import AuthenticateUseCase, AuthenticateRequest

auth_app = typer.Typer()
console = Console()

@auth_app.callback()
def access(ctx: typer.Context):
    """Callback - for login & logout commands, verify token presence """
    token = TokenStore.has_token()
    if ctx.invoked_subcommand == "login":
        if token:
            console.print("[green]Vous êtes déjà connecté[/green]")
            raise typer.Exit(1)
    if ctx.invoked_subcommand == "logout":
        if not token:
            console.print("[red]Vous n'êtes pas connecté[/red]")
            raise typer.Exit(1)

@auth_app.command()
def login(ctx: typer.Context,
        email: str = typer.Option(prompt=True),
        password: str = typer.Option(prompt=True, hide_input=True)
):
    """Connect user to email & password"""
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    password_hasher = BcryptPasswordHasher()
    token_manager = JWTTokenManager()
    use_case = AuthenticateUseCase(repo, password_hasher, token_manager)

    request = AuthenticateRequest(email, password)
    response = use_case.execute(request)
    if response.success is False:
        console.print(f"{response.error}")
    else:
        console.print("[green]Vous êtes connecté[/green]")

@auth_app.command()
def logout():
    """Logout user"""
    token_storage = TokenStore()
    if token_storage.has_token():
        token_storage.delete_token()
        console.print("[green]Vous êtes déconnecté[/green]")

