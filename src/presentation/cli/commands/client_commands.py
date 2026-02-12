from typing import Optional, List

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from helpers.helper_cli import error_display
from helpers.helpers import normalize

from src.domain.entities.entities import  Client
from src.domain.policies.user_policy import RequestPolicy, UserPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyClientRepository
from src.use_cases.client_use_cases import GetClientUseCase, GetClientRequest, CreateClientRequest, CreateClientUseCase, \
    ListClientUseCase, UpdateClientRequest, UpdateClientUseCase, DeleteClientUseCase, DeleteClientRequest, \
    ListClientRequest, ClientFilter

client_app = typer.Typer()
console = Console()

@client_app.callback()
def permission(ctx:typer.Context):
    """Callback - verify user role """
    ctx.obj["ressource"] = "CLIENT"

    action = ctx.invoked_subcommand
    if action in ["list", "show"]:
        return

    request = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action=action,
        context=None
    )

    policy = UserPolicy(request)
    if not policy.is_allowed():
        error_display("Permission", "Vous êtes pas authorisé à utiliser cette commande")
        raise typer.Exit(1)

@client_app.command()
def create(
        ctx: typer.Context,
        fullname: str = typer.Option(prompt=True),
        email: str = typer.Option(prompt=True),
        telephone: str = typer.Option(prompt=True),
        company_name: str = typer.Option(prompt=True),
):
    """
    Creates new client
    :param ctx: context typer
    :param fullname: fullname client
    :param email: email client
    :param telephone: telephone number client
    :param company_name: name of company client
    :return: None
    """
    # Requête pour l'authorisation
    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="create",
    )

    # Requête avec les données necessaire Use Case
    request = CreateClientRequest(
        fullname=fullname,
        email=email,
        telephone=telephone,
        company_name=company_name,
        authorization= policy,
    )

    # Use case
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = CreateClientUseCase(repo)
    response = use_case.execute(request)

    # Affichage selon response.success
    if response.success:
        console.print(f"\n[bold]Client #{response.client.id} créé[/bold]\n")
        _display_data(response.client)
    else:
        error_display(response.error, response.msg)

@client_app.command()
def update(ctx: typer.Context, client_id: int):
    """
    Command for update client
    :param ctx: typer Context
    :param client_id: ID of client
    :return: None
    """
    # init
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = UpdateClientUseCase(repo)

    #verification ressource existe
    client = repo.find_by_id(client_id)
    if not client:
        error_display("Ressource","Client non trouvé")
        raise typer.Exit(1)

    if client.commercial_contact_id != ctx.obj["current_user"]["user_current_id"]:
        error_display("Permission", "Seuls les membres commerciaux associé au client peuvent le modifier")
        raise typer.Exit(1)

    # requete autorisation
    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="update",
    )


    fullname = typer.prompt('Nom complet ', default='', show_default=False)
    email= typer.prompt('Email ', default='',show_default=False)
    telephone= typer.prompt('Téléphone ', default='',show_default=False)
    company_name= typer.prompt("Nom de l'entreprise ", default='',show_default=False)

    fullname = normalize(fullname)
    email = normalize(email)
    telephone = normalize(telephone)
    company_name = normalize(company_name)

    request = UpdateClientRequest(
        client_id=client_id,
        fullname=fullname,
        email=email,
        telephone=telephone,
        company_name=company_name,
        authorization= policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Client #{response.client.id} modifié[/bold]\n")
        _display_data(response.client)
    else:
        error_display(response.error, response.msg)


@client_app.command()
def show(ctx: typer.Context, client_id: int):
    """
    Command for show client
    :param ctx: typer Context
    :param client_id: ID of client
    :return: None
    """
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = GetClientUseCase(repo)

    # verification ressource existante
    if not repo.exist(client_id):
        error_display("Ressource", "Client non trouvé")
        raise typer.Exit()

    request = GetClientRequest(
        client_id=client_id,
    )
    response = use_case.execute(request)

    if response.success:
        _display_data(response.client)
    else:
        error_display(response.error, response.msg)

@client_app.command()
def list(
        ctx: typer.Context,
        list_filter: Optional[ClientFilter] = typer.Option(
            None, "--filter","-f",
            help="Filter clients (mine)",
        ),
):
    """
    Command for list clients
    :param list_filter: filter list
    :param ctx: typer Context
    :return: None
    """

    request = ListClientRequest(
        user_id=ctx.obj["current_user"]["user_current_id"],
        list_filter=list_filter
    )
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = ListClientUseCase(repo)
    response = use_case.execute(request)

    if response.success:
        _display_data_list(response.clients, list_filter)
    else:
        error_display(response.error, response.msg)

@client_app.command()
def delete(ctx: typer.Context, client_id: int, ):
    """
    Command for delete client
    :param ctx: typer Context
    :param client_id: ID of client
    :return: None
    """
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = DeleteClientUseCase(repo)

    #verification ressource existe
    if not repo.exist(client_id):
        error_display("Permission","Client non trouvé")
        raise typer.Exit()

    if not typer.confirm(f"Etes-vous sure de vouloir supprimer le Client #{client_id} ?"):
        error_display("Annulation", "Suppression du client annulé")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="delete"
    )
    request = DeleteClientRequest(
        client_id=client_id,
        authorization= policy,
    )

    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Client #{client_id} supprimé[/bold]")
    else:
        error_display(response.error, response.msg)

def _display_data(client: Client):
    """ Display data of Client """

    content = Text()

    content.append(f"\nID: ", style="bold cyan")
    content.append(f"{client.id or 'N/A'}\n")

    content.append(f"Adresse email: ", style="bold cyan")
    content.append(f"{client.email}\n")

    content.append(f"Téléphone: ", style="bold cyan")
    content.append(f"{client.telephone}\n")

    content.append(f"Nom de l'entreprise: ", style="bold cyan")
    content.append(f"{client.company_name}\n")

    content.append(f"Contact commercial: ", style="bold cyan")
    content.append(f"{client.commercial_contact_id}\n")

    panel = Panel(
        content,
        title=f"[bold magenta] {client.fullname}[/bold magenta]",
        border_style="white",
        box=box.ROUNDED,
        expand=False
    )

    console.print(panel)

def _display_data_list(clients: List[Client], filtre: ClientFilter):
    """
    Display clients table
    """
    filtre = filtre.name if filtre else None
    table = Table(
        title=f"[bold magenta] Liste des Clients - filtre: {filtre}[/bold magenta]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="white"
    )

    table.add_column("ID", style="dim", width=6, justify="right")
    table.add_column("Nom complet", style="bold", min_width=20)
    table.add_column("Email", width=16)
    table.add_column("Téléphone", width=16)
    table.add_column("Non de l'entreprise", min_width=15)
    table.add_column("Contact commercial", width=12, justify="right")

    for client in clients:

        table.add_row(
            str(client.id or "-"),
            client.fullname,
            str(client.email),
            str(client.telephone),
            client.company_name,
            str(client.commercial_contact_id),
        )
    console.print(f"\nTotal: [dim]{len(clients)} client(s)[/dim]")
    console.print(table)