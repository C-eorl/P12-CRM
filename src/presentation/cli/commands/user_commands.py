from typing import Optional

import typer
from rich.console import Console

from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher
from src.use_cases.user_use_cases import CreateUserRequest, CreateUserUseCase, UpdateUserRequest, UpdateUserUseCase, \
    GetUserRequest, GetUserUseCase, ListUserUseCase

user_app = typer.Typer()
console = Console()

@user_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.obj["current_user"]["user_role"] != Role.GESTION:
            console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
            raise typer.Exit()

@user_app.command()
def create(
        ctx: typer.Context,
        fullname: str = typer.Option(..., prompt=True),
        email: str = typer.Option(..., prompt=True),
        password: str = typer.Option(..., prompt=True),
        role: Role = typer.Option(..., prompt=True),
):

    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    hash_password = BcryptPasswordHasher()

    request = CreateUserRequest(
        fullname=fullname,
        email=email,
        password=password,
        role=role,
        current_user=ctx.obj["current_user"]
    )
    use_case = CreateUserUseCase(repo, hash_password)
    response = use_case.execute(request)

    console.print(f"\n[bold]Utilisateur #{response.user.id} créé[/bold]")
    _display_data(response.user)

@user_app.command()
def update(
        ctx: typer.Context,
        client_id: int,
        fullname: Optional[str] = typer.Option('', prompt=True, show_default=False),
        email: Optional[str] = typer.Option('', prompt=True, show_default=False)
        ):

    def normalize(value: str | None) -> str | None:
        return value if value != '' else None

    fullname = normalize(fullname)
    email = normalize(email)

    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    request = UpdateUserRequest(
        user_id=client_id,
        fullname=fullname,
        email=email,
        current_user=ctx.obj["current_user"]
    )
    use_case = UpdateUserUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Utilisateur #{response.user.id} modifié[/bold]")
    _display_data(response.user)


@user_app.command()
def show(ctx: typer.Context, user_id: int):

    repo = SQLAlchemyUserRepository(ctx.obj["session"])

    request = GetUserRequest(
        user_id=user_id,
        current_user = ctx.obj["current_user"]
    )
    use_case = GetUserUseCase(repo)
    response = use_case.execute(request)


    console.print(f"\n[bold]Utilisateur #{response.user.id}[/bold]")
    _display_data(response.user)

@user_app.command()
def list(ctx: typer.Context):
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    use_case = ListUserUseCase(repo)

    response = use_case.execute()

    for user in response.users:
        console.print(f"\n[bold]Client #{user.id}[/bold]")
        _display_data(user)


def _display_data(data: User):

    console.print(f"  Nom: {data.fullname}")
    console.print(f"  Email: {data.email}")
    console.print(f"  Role: {data.role}")
    console.print(f"  Créé le: {data.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {data.updated_at.strftime('%d/%m/%Y %H:%M')}\n")