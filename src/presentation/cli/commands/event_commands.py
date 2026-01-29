from datetime import datetime
from typing import Optional

import typer
from rich.console import Console

from src.domain.entities.entities import User, Event
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyEventRepository, SQLAlchemyUserRepository
from src.use_cases.event_use_cases import ListEventUseCase, GetEventUseCase, GetEventRequest, UpdateEventUseCase, \
    UpdateEventRequest, CreateEventUseCase, CreateEventRequest, AssignSupportEventRequest, AssignSupportEventUseCase

event_app = typer.Typer()
console = Console()

@event_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.invoked_subcommand == "assign":
            if ctx.obj["current_user"]["user_role"] != Role.GESTION:
                console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
                raise typer.Exit()

        if ctx.invoked_subcommand == "create":
            if ctx.obj["current_user"]["user_role"] != Role.COMMERCIAL:
                console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
                raise typer.Exit()

        if ctx.invoked_subcommand == "update":
            if ctx.obj["current_user"]["user_role"] != Role.SUPPORT:
                console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
                raise typer.Exit()

@event_app.command(help="Créer un évènement")
def create(
        ctx: typer.Context,
        name: str = typer.Option(..., prompt=True),
        contrat_id: int = typer.Option(..., prompt=True),
        client_id: int = typer.Option(..., prompt=True),
        support_contact_id: Optional[int] = typer.Option(..., prompt=True),
        start_date: datetime = typer.Option(..., prompt=True),
        end_date: datetime = typer.Option(..., prompt=True),
        location: str = typer.Option(..., prompt=True),
        attendees: int = typer.Option(..., prompt=True),
        notes: str = typer.Option(..., prompt=True),
):

    repo = SQLAlchemyEventRepository(ctx.obj["session"])

    request = CreateEventRequest(
        name= name,
        contrat_id = contrat_id,
        client_id = client_id,
        support_contact_id = support_contact_id,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        current_user =  ctx.obj["current_user"]
    )
    use_case = CreateEventUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Évènement #{response.event.id} créé[/bold]")
    _display_data(response.event)

@event_app.command(help="Modifier un évènement")
def update(
        ctx: typer.Context,
        event_id: int,
        name: str = typer.Option('', prompt=True),
        start_date: datetime = typer.Option('', prompt=True, ),
        end_date: datetime = typer.Option('', prompt=True),
        location: str = typer.Option('', prompt=True),
        attendees: int = typer.Option(0, prompt=True),
        notes: str = typer.Option('', prompt=True),
        ):

    def normalize(value: str | None) -> str | None:
        return value if value not in ('', 0) else None

    name = normalize(name)
    location = normalize(location)
    attendees = normalize(attendees)
    notes = normalize(notes)

    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    request = UpdateEventRequest(
        event_id=event_id,
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        current_user=ctx.obj["current_user"]
    )
    use_case = UpdateEventUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Évènement #{response.event.id} modifié[/bold]")
    _display_data(response.event)


@event_app.command(help="Afficher un évènement")
def show(ctx : typer.Context, event_id: int):

    repo = SQLAlchemyEventRepository(ctx.obj["session"])

    request = GetEventRequest(
        event_id=event_id,
        current_user= ctx.obj["current_user"]
    )
    use_case = GetEventUseCase(repo)
    response = use_case.execute(request)


    console.print(f"\n[bold]Évènement #{response.event.id}[/bold]")
    _display_data(response.event)

@event_app.command(help="Afficher tous les évènement")
def list(ctx: typer.Context):
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = ListEventUseCase(repo)

    response = use_case.execute()

    for event in response.events:
        console.print(f"\n[bold]Client #{event.id}[/bold]")
        _display_data(event)

@event_app.command(help="Assigner un Utilisateur Support a l'évènement")
def assign(
        ctx: typer.Context,
        event_id: int,
        support_user_id: int = typer.Option(None),
        ):

    session = ctx.obj["session"]
    repo = SQLAlchemyEventRepository(session)
    user_repo = SQLAlchemyUserRepository(session)
    request = AssignSupportEventRequest(
        event_id=event_id,
        support_user_id=support_user_id,
        current_user=User(
            id=5,
            fullname="test test",
            email=Email("test@test.com"), password="sfsefs",
            role=Role.GESTION
        )
    )
    use_case = AssignSupportEventUseCase(repo, user_repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Évènement #{event_id} - assigné à User #: {support_user_id}[bold]")


def _display_data(data: Event):

    console.print(f"  Nom: ID {data.name}")
    console.print(f"  Contrat: ID {data.contrat_id}")
    console.print(f"  Client: ID {data.client_id}")
    console.print(f"  Contact support: ID {data.support_contact_id}")
    console.print(f"  Date de début: {data.start_date.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Date de fin: {data.end_date.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Emplacement: {data.location}")
    console.print(f"  Participants: {data.attendees}")
    console.print(f"  Notes: {data.notes}")
    console.print(f"  Créé le: {data.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {data.updated_at.strftime('%d/%m/%Y %H:%M')}\n")