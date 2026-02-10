from typing import Optional, List

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from helpers.helpers import normalize
from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher
from src.use_cases.user_use_cases import CreateUserRequest, CreateUserUseCase, UpdateUserRequest, UpdateUserUseCase, \
    GetUserRequest, GetUserUseCase, ListUserUseCase, DeleteUserUseCase, DeleteUserRequest, ListUserRequest, UserFilter

user_app = typer.Typer()
console = Console()

@user_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.obj["current_user"]["user_current_role"] not in [Role.GESTION, Role.ADMIN]:
            console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
            raise typer.Exit()
    ctx.obj["ressource"] = "USER"

@user_app.command(help="Créer un utilisateur")
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

@user_app.command(help="Modifier un utilisateur")
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

@user_app.command(help="Afficher un utilisateur")
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
        console.print(f"\n[bold]Utilisateur #{response.user.id}[/bold]\n")
        _display_data(response.user)
    else:
        console.print(f"[red] {response.error} [/red]")

@user_app.command(help="Afficher une liste d'utilisateur")
def list(
        ctx: typer.Context,
        list_filter: Optional[UserFilter] = typer.Option(
            None, "--filter", "-f",
            help="Filter user (commercial, gestion, support)",
        ),
):
    """
    Command to list all users
    :param list_filter: list filters
    :param ctx: typer context
    :return: None
    """

    request = ListUserRequest(
        list_filter=list_filter,
    )


    repo = SQLAlchemyUserRepository(ctx.obj["session"])
    use_case = ListUserUseCase(repo)
    response = use_case.execute(request)

    if response.success:
        _display_data_list(response.users)
    else:
        console.print(f"[red] {response.error} [/red]")

@user_app.command(help="Supprimer un utilisateur")
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
        console.print(f"[red] Utilisateur non trouvé [/red]")
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

def _display_data(user: User):
    """ Display data of User """
    content = Text()

    content.append(f"\nID: ", style="bold cyan")
    content.append(f"{user.id or 'N/A'}\n")

    content.append(f"Nom complet: ", style="bold cyan")
    content.append(f"{user.fullname}\n")

    content.append(f"Adresse Email: ", style="bold cyan")
    content.append(f"{user.email}\n")

    content.append(f"Role: ", style="bold cyan")
    content.append(f"{user.role.name}\n")

    panel = Panel(
        content,
        title=f"[bold magenta] {user.fullname}[/bold magenta]",
        border_style="white",
        box=box.ROUNDED,
        expand=False
    )

    console.print(panel)

def _display_data_list(users: List[User]):
    """
    Display users table
    """

    table = Table(
        title="[bold magenta] Liste des Utilisateurs[/bold magenta]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="white"
    )

    table.add_column("ID", style="dim", width=6, justify="right")
    table.add_column("Nom complet", style="bold", min_width=20)
    table.add_column("Email", width=16)
    table.add_column("Role", width=16)

    for user in users:

        table.add_row(
            str(user.id or "-"),
            user.fullname,
            str(user.email),
            user.role.name,
        )
    console.print(f"\nTotal: [dim]{len(users)} utilisateur(s)[/dim]")
    console.print(table)