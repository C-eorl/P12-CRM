from typing import Optional

import typer
from rich.console import Console

from helpers.helpers import normalize

from src.domain.entities.entities import  Client
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyClientRepository
from src.use_cases.client_use_cases import GetClientUseCase, GetClientRequest, CreateClientRequest, CreateClientUseCase, \
    ListClientUseCase, UpdateClientRequest, UpdateClientUseCase, DeleteClientUseCase, DeleteClientRequest, \
    ListClientRequest, ClientFilter

client_app = typer.Typer()
console = Console()

@client_app.callback()
def permission(ctx:typer.Context):
    """Callback - for show, list commands, verify user role """
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.obj["current_user"]["user_current_role"] not in  [Role.COMMERCIAL, Role.ADMIN]:
            console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
            raise typer.Exit()
    ctx.obj["ressource"] = "CLIENT"

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
        console.print(f"\n[bold]Client #{response.client.id} créé[/bold]")
        _display_data(response.client)
    else:
        console.print(f"[red] {response.error} [/red]")

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
    if not repo.exist(client_id):
        console.print(f"[red] Client non trouvé [/red]")
        raise typer.Exit()
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
        console.print(f"\n[bold]Client #{response.client.id} modifié[/bold]")
        _display_data(response.client)
    else:
        console.print(f"[red] {response.error} [/red]")


@client_app.command()
def show(ctx: typer.Context, client_id: int):
    """
    Command for show one client
    :param ctx: typer Context
    :param client_id: ID of client
    :return: None
    """
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = GetClientUseCase(repo)

    #verification ressource existe
    if not repo.exist(client_id):
        console.print(f"[red] Client non trouvé [/red]")
        raise typer.Exit()

    request = GetClientRequest(
        client_id=client_id,
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Client #{response.client.id}[/bold]")
        _display_data(response.client)
    else:
        console.print(f"[red] {response.error} [/red]")

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
        console.print(f"Clients trouvés : {len(response.clients)}")
        for client in response.clients:
            console.print(f"\n[bold]Client #{client.id}[/bold]")
            _display_data(client)
    else:
        console.print(f"[red] {response.error} [/red]")

@client_app.command()
def delete(ctx: typer.Context, client_id: int):
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
        console.print(f"[red] Client non trouvé [/red]")
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
        console.print(f"[red] {response.error} [/red]")

def _display_data(data: Client):
    """ Display data of Client """

    console.print(f"  Nom: {data.fullname}")
    console.print(f"  Email: {data.email}")
    console.print(f"  Téléphone: {data.telephone}")
    console.print(f"  Entreprise: {data.company_name}")
    console.print(f"  Commercial: ID {data.commercial_contact_id}")
    console.print(f"  Créé le: {data.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {data.updated_at.strftime('%d/%m/%Y %H:%M')}\n")