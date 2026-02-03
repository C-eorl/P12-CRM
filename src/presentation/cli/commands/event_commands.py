from datetime import datetime
from typing import Optional

import typer
from rich.console import Console

from helpers.helpers import normalize
from src.domain.entities.entities import Event
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyEventRepository, SQLAlchemyUserRepository
from src.use_cases.event_use_cases import ListEventUseCase, GetEventUseCase, GetEventRequest, UpdateEventUseCase, \
    UpdateEventRequest, CreateEventUseCase, CreateEventRequest, AssignSupportEventRequest, AssignSupportEventUseCase

event_app = typer.Typer()
console = Console()

@event_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.invoked_subcommand == "assign":
            if ctx.obj["current_user"]["user_role"] not in [Role.GESTION, Role.ADMIN]:
                console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
                raise typer.Exit()

        if ctx.invoked_subcommand == "create":
            if ctx.obj["current_user"]["user_role"] not in [Role.COMMERCIAL, Role.ADMIN]:
                console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
                raise typer.Exit()

        if ctx.invoked_subcommand == "update":
            if ctx.obj["current_user"]["user_role"] not in [Role.SUPPORT, Role.ADMIN]:
                console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
                raise typer.Exit()
    ctx.obj["ressource"] = "EVENT"

@event_app.command(help="Créer un évènement")
def create(
        ctx: typer.Context,
        name: str = typer.Option(None, prompt=True),
        contrat_id: int = typer.Option(None, prompt=True),
        client_id: int = typer.Option(None, prompt=True),
        support_contact_id: Optional[int] = typer.Option("", prompt=True),
        start_date: datetime = typer.Option(..., prompt=True),
        end_date: datetime = typer.Option(..., prompt=True),
        location: str = typer.Option(..., prompt=True),
        attendees: int = typer.Option(..., prompt=True),
        notes: str = typer.Option(..., prompt=True),
):
    """
    Command for create Event
    :param ctx: typer.Context
    :param name: name of the event
    :param contrat_id: ID contrat linked to the event
    :param client_id: ID client linked to the event
    :param support_contact_id: ID support contact linked to the event
    :param start_date: start date of the event
    :param end_date: end date of the event
    :param location: location of the event
    :param attendees: number of attendees
    :param notes: various notes
    :return: None
    """
    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="create"
    )

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
        authorization=policy
    )
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = CreateEventUseCase(repo)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Evènement #{response.event.id} créé[/bold]")
        _display_data(response.event)
    else:
        console.print(f"[red] {response.error} [/red]")


@event_app.command(help="Modifier un évènement")
def update(ctx: typer.Context, event_id: int):
    """
    Command for update Event
    :param ctx: typer.Context
    :param event_id: ID of the event
    :return: None
    """
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = UpdateEventUseCase(repo)

    if not repo.exist(event_id):
        console.print(f"[red] Client non trouvé [/red]")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="update"
    )

    name = typer.prompt("Nom de l'évènement: ", "")
    start_date= typer.prompt('Date et heure de début (2000-00-00 00:00:00): ', "")
    end_date = typer.prompt('Date et heure de fin (2000-00-00 00:00:00): ', "")
    location = typer.prompt('Emplacement: ', "")
    attendees = typer.prompt("Nombre de participant: ", "")
    notes = typer.prompt("Notes: ", "")

    name = normalize(name)
    location = normalize(location)
    attendees = normalize(attendees)
    notes = normalize(notes)

    request = UpdateEventRequest(
        event_id=event_id,
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Evènement #{response.event.id} modifié[/bold]")
        _display_data(response.event)
    else:
        console.print(f"[red] {response.error} [/red]")


@event_app.command(help="Afficher un évènement")
def show(ctx : typer.Context, event_id: int):
    """
    Command for show one Event
    :param ctx:  typer.Context
    :param event_id: ID of the event
    :return: None
    """

    request = GetEventRequest(
        event_id=event_id,
    )
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = GetEventUseCase(repo)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Evènement #{response.event.id}[/bold]")
        _display_data(response.event)
    else:
        console.print(f"[red] {response.error} [/red]")

@event_app.command(help="Afficher tous les évènement")
def list(ctx: typer.Context):
    """
    Command for list Event
    :param ctx: typer.Context
    :return: None
    """
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = ListEventUseCase(repo)
    response = use_case.execute()

    if response.success:
        for event in response.events:
            console.print(f"\n[bold]Client #{event.id}[/bold]")
            _display_data(event)
    else:
        console.print(f"[red] {response.error} [/red]")


@event_app.command(help="Assigner un Utilisateur Support a l'évènement")
def assign(ctx: typer.Context, event_id: int):
    """
    Command for assign user support to event
    :param ctx: typer Context
    :param event_id: ID of the event
    :return: None
    """
    session = ctx.obj["session"]
    repo = SQLAlchemyEventRepository(session)
    user_repo = SQLAlchemyUserRepository(session)

    if not repo.exist(event_id):
        console.print(f"[red] Client non trouvé [/red]")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="assign"
    )

    support_user_id= typer.prompt("Id utilisateur Support: "),

    request = AssignSupportEventRequest(
        event_id=event_id,
        support_user_id=int(support_user_id),
        authorization=policy
    )
    use_case = AssignSupportEventUseCase(repo, user_repo)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Évènement #{event_id} - assigné à User #: {support_user_id}[bold]")
    else:
        console.print(f"[red] {response.error} [/red]")
    console.print(f"\n[bold]Évènement #{event_id} - assigné à User #: {support_user_id}[bold]")


def _display_data(data: Event):
    """ Display data of Event"""
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