from typing import Optional

import typer
from rich.console import Console

from helpers.helpers import normalize
from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher
from src.use_cases.user_use_cases import CreateUserRequest, CreateUserUseCase, UpdateUserRequest, UpdateUserUseCase, \
    GetUserRequest, GetUserUseCase, ListUserUseCase, DeleteUserUseCase, DeleteUserRequest

user_app = typer.Typer()
console = Console()

@user_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.obj["current_user"]["user_current_role"] not in [Role.GESTION, Role.ADMIN]:
            console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
            raise typer.Exit()
    ctx.obj["ressource"] = "USER"

@user_app.command()
def create(
        ctx: typer.Context,
        fullname: str = typer.Option(..., prompt=True),
        email: str = typer.Option(..., prompt=True),
        password: str = typer.Option(..., prompt=True),
        role: Role = typer.Option(..., prompt=True),
):
    """
    Command to create new user
    :param ctx: typer context
    :param fullname: full name for user
    :param email: email for user
    :param password: password for user
    :param role: role for user
    :return: None
    """
    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource= ctx.obj["ressource"],
        action="create",
    )
    request = CreateUserRequest(
        fullname=fullname,
        email=email,
        password=password,
        role=role,
        authorization=policy
    )
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    hash_password = BcryptPasswordHasher()
    use_case = CreateUserUseCase(repo, hash_password)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Utilisateur #{response.user.id} créé[/bold]")
        _display_data(response.user)
    else:
        console.print(f"[red] {response.error} [/red]")

@user_app.command()
def update(ctx: typer.Context, user_id: int):
    """
    Command to update existing user
    :param ctx: typer context
    :param user_id: ID of user
    :return: None
    """
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    use_case = UpdateUserUseCase(repo)

    if not repo.exist(user_id):
        console.print(f"[red] Utilisateur non trouvé [/red]")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource= ctx.obj["ressource"],
        action="update",
    )

    fullname: Optional[str] = typer.prompt('Nom complet: ', "")
    email: Optional[str] = typer.prompt('Email: ', "")

    fullname = normalize(fullname)
    email = normalize(email)

    request = UpdateUserRequest(
        user_id=user_id,
        fullname=fullname,
        email=email,
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Utilisateur #{response.user.id} modifié[/bold]")
        _display_data(response.user)
    else:
        console.print(f"[red] {response.error} [/red]")

@user_app.command()
def show(ctx: typer.Context, user_id: int):
    """
    Command to show a user
    :param ctx: typer contact
    :param user_id: ID of user
    :return: None
    """

    request = GetUserRequest(
        user_id=user_id,
    )
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    use_case = GetUserUseCase(repo)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Utilisateur #{response.user.id}[/bold]")
        _display_data(response.user)
    else:
        console.print(f"[red] {response.error} [/red]")

@user_app.command()
def list(ctx: typer.Context):
    """
    Command to list all users
    :param ctx: typer context
    :return: None
    """
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    use_case = ListUserUseCase(repo)
    response = use_case.execute()

    if response.success:
        for user in response.users:
            console.print(f"\n[bold]Utilisateur #{user.id}[/bold]")
            _display_data(user)
    else:
        console.print(f"[red] {response.error} [/red]")

@user_app.command()
def delete(ctx: typer.Context, user_id: int):
    """
    Command for delete client
    :param ctx: typer Context
    :param user_id: ID of user
    :return: None
    """
    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    use_case = DeleteUserUseCase(repo)

    #verification ressource existe
    if not repo.exist(user_id):
        console.print(f"[red] Client non trouvé [/red]")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="delete"
    )
    request = DeleteUserRequest(
        user_id=user_id,
        authorization= policy,
    )

    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Utilisateur #{user_id} supprimé[/bold]")
    else:
        console.print(f"[red] {response.error} [/red]")

def _display_data(data: User):
    """ Display data of User """
    console.print(f"  Nom: {data.fullname}")
    console.print(f"  Email: {data.email}")
    console.print(f"  Role: {data.role}")
    console.print(f"  Créé le: {data.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {data.updated_at.strftime('%d/%m/%Y %H:%M')}\n")