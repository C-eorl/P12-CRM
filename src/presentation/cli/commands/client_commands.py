from typing import Optional

import typer
from rich.console import Console

from src.domain.entities.entities import User, Client
from src.domain.entities.enums import Role
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyClientRepository
from src.use_cases.client_use_cases import GetClientUseCase, GetClientRequest, CreateClientRequest, CreateClientUseCase, \
    ListClientUseCase, UpdateClientRequest, UpdateClientUseCase

client_app = typer.Typer()
console = Console()

@client_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.obj["current_user"]["user_role"] != Role.COMMERCIAL:
            console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
            raise typer.Exit()


@client_app.command()
def create(
        ctx: typer.Context,
        fullname: str = typer.Option(..., prompt=True),
        email: str = typer.Option(..., prompt=True),
        telephone: str = typer.Option(..., prompt=True),
        company_name: str = typer.Option(..., prompt=True),
):

    repo = SQLAlchemyClientRepository(ctx.obj["session"])

    request = CreateClientRequest(
        fullname=fullname,
        email=email,
        telephone=telephone,
        company_name=company_name,
        current_user= ctx.obj["current_user"],
    )
    use_case = CreateClientUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Client #{response.client.id} créé[/bold]")
    _display_data(response.client)

@client_app.command()
def update(ctx: typer.Context,
           client_id: int,
           fullname: Optional[str] = typer.Option('', prompt=True, show_default=False),
           email: Optional[str] = typer.Option('', prompt=True, show_default=False),
           telephone: Optional[str] = typer.Option('', prompt=True, show_default=False),
           company_name: Optional[str] = typer.Option('', prompt=True, show_default=False),
           ):

    def normalize(value: str | None) -> str | None:
        return value if value != '' else None

    fullname = normalize(fullname)
    email = normalize(email)
    telephone = normalize(telephone)
    company_name = normalize(company_name)



    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    request = UpdateClientRequest(
        client_id=client_id,
        fullname=fullname,
        email=email,
        telephone=telephone,
        company_name=company_name,
        current_user=ctx.obj["current_user"]
    )
    use_case = UpdateClientUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Client #{response.client.id} modifié[/bold]")
    _display_data(response.client)


@client_app.command()
def show(
        ctx: typer.Context,
        client_id: int
):

    repo = SQLAlchemyClientRepository(ctx.obj["session"])

    request = GetClientRequest(
        client_id=client_id,
        current_user= ctx.obj["current_user"]
    )
    use_case = GetClientUseCase(repo)
    response = use_case.execute(request)


    console.print(f"\n[bold]Client #{response.client.id}[/bold]")
    _display_data(response.client)

@client_app.command()
def list(ctx: typer.Context):
    repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = ListClientUseCase(repo)

    response = use_case.execute()

    for client in response.clients:
        console.print(f"\n[bold]Client #{client.id}[/bold]")
        _display_data(client)


def _display_data(data: Client):

    console.print(f"  Nom: {data.fullname}")
    console.print(f"  Email: {data.email}")
    console.print(f"  Téléphone: {data.telephone}")
    console.print(f"  Entreprise: {data.company_name}")
    console.print(f"  Commercial: ID {data.commercial_contact_id}")
    console.print(f"  Créé le: {data.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {data.updated_at.strftime('%d/%m/%Y %H:%M')}\n")