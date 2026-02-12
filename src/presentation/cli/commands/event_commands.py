from datetime import datetime
from typing import Optional, List

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from helpers.helper_cli import error_display
from helpers.helpers import normalize
from src.domain.entities.entities import Event
from src.domain.entities.enums import Role
from src.domain.policies.user_policy import RequestPolicy, UserPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyEventRepository, SQLAlchemyUserRepository, \
    SQLAlchemyContratRepository, SQLAlchemyClientRepository
from src.use_cases.event_use_cases import ListEventUseCase, GetEventUseCase, GetEventRequest, UpdateEventUseCase, \
    UpdateEventRequest, CreateEventUseCase, CreateEventRequest, AssignSupportEventRequest, AssignSupportEventUseCase, \
    EventFilter, ListEventRequest, DeleteEventRequest, DeleteEventUseCase

event_app = typer.Typer()
console = Console()

@event_app.callback()
def permission(ctx:typer.Context):
    """Callback - verify user role """
    ctx.obj["ressource"] = "EVENT"
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


@event_app.command(help="Créer un évènement")
def create(
        ctx: typer.Context,
        name: str = typer.Option(None, prompt=True),
        contrat_id: int = typer.Option(None, prompt=True),
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
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        authorization=policy
    )
    event_repo = SQLAlchemyEventRepository(ctx.obj["session"])
    contrat_repo = SQLAlchemyContratRepository(ctx.obj["session"])
    client_repo = SQLAlchemyClientRepository(ctx.obj["session"])
    use_case = CreateEventUseCase(event_repo, contrat_repo, client_repo)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Evènement #{response.event.id} créé[/bold]\n")
        _display_data(response.event)
    else:
        error_display(response.error, response.msg)


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

    event = repo.find_by_id(event_id)
    if not event:
        error_display("Permission", "Evènement non trouvé")
        raise typer.Exit()

    if event.support_contact_id != ctx.obj["current_user"]["user_current_role"]:
        error_display("Permission", "Seuls les membres support associé à l'évènement peuvent le modifier")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="update"
    )

    name = typer.prompt("Nom de l'évènement: ", "", show_default=False)
    start_date= typer.prompt('Date et heure de début (2000-00-00 00:00:00): ', "", show_default=False)
    end_date = typer.prompt('Date et heure de fin (2000-00-00 00:00:00): ', "", show_default=False)
    location = typer.prompt('Emplacement: ', "", show_default=False)
    attendees = typer.prompt("Nombre de participant: ", "", show_default=False)
    notes = typer.prompt("Notes: ", "", show_default=False)

    name = normalize(name)
    location = normalize(location)
    attendees = normalize(attendees)
    notes = normalize(notes)

    request = UpdateEventRequest(
        event_id=event_id,
        name=name,
        start_date=datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
        end_date=datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S"),
        location=location,
        attendees=int(attendees),
        notes=notes,
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Evènement #{response.event.id} modifié[/bold]\n")
        _display_data(response.event)
    else:
        error_display(response.error, response.msg)


@event_app.command(help="Afficher un évènement")
def show(ctx : typer.Context, event_id: int):
    """
    Command for show Event
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
        _display_data(response.event)
    else:
        error_display(response.error, response.msg)

@event_app.command(help="Afficher tous les évènement")
def list(
        ctx: typer.Context,
        list_filter: Optional[EventFilter] = typer.Option(
            None, "--filter", "-f",
            help="Filter events"
        )
    ):
    """
    Command for list Event
    :param list_filter: filter event
    :param ctx: typer.Context
    :return: None
    """
    request = ListEventRequest(
        support_contact_id= ctx.obj["current_user"]["user_current_id"],
        list_filter=list_filter,
    )
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = ListEventUseCase(repo)
    response = use_case.execute(request)

    if response.success:
        _display_data_list(response.events, list_filter)
    else:
        error_display(response.error, response.msg)


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
        error_display("Ressource", "Client non trouvé")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="assign"
    )

    support_user_id= typer.prompt("Id utilisateur Support: ")

    request = AssignSupportEventRequest(
        event_id=event_id,
        support_user_id=int(support_user_id),
        authorization=policy
    )
    use_case = AssignSupportEventUseCase(repo, user_repo)
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Évènement #{event_id} - assigné à User #: {support_user_id}[bold]\n")
    else:
        error_display(response.error, response.msg)

@event_app.command(help="Supprimer un évènement")
def delete(ctx: typer.Context, event_id: int):
    """
    Command for delete contrat
    :param ctx: typer Context
    :param event_id: ID of contrat
    :return: None
    """
    repo = SQLAlchemyEventRepository(ctx.obj["session"])
    use_case = DeleteEventUseCase(repo)

    #verification ressource existe
    if not repo.exist(event_id):
        error_display("Ressource", "Evènement non trouvé")
        raise typer.Exit()

    if not typer.confirm(f"Etes-vous sure de vouloir supprimer l'Evènement #{event_id} ?"):
        error_display("Annulation", "Suppression de l'évènement annulé")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="delete"
    )
    request = DeleteEventRequest(
        event_id=event_id,
        authorization= policy,
    )

    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Evènement #{event_id} supprimé[/bold]")
    else:
        error_display(response.error, response.msg)


def _display_data(event: Event):
    """ Display data of Event"""

    content = Text()

    content.append(f"ID: ", style="bold cyan")
    content.append(f"{event.id or 'N/A'}\n")

    content.append(f"\nContrat: ", style="bold cyan")
    content.append(f"#{event.contrat_id}\n")

    content.append(f"Client: ", style="bold cyan")
    content.append(f"#{event.client_id}\n")

    content.append(f"Contact Support: ", style="bold cyan")
    support_text = f"#{event.support_contact_id}" if event.support_contact_id else "Non assigné"
    content.append(support_text + "\n")

    content.append(f"\nDébut: ", style="bold cyan")
    content.append(f"{event.start_date.strftime('%d/%m/%Y %H:%M')}\n")

    content.append(f"Fin: ", style="bold cyan")
    content.append(f"{event.end_date.strftime('%d/%m/%Y %H:%M')}\n")


    content.append(f"\nLieu: ", style="bold cyan")
    content.append(f"{event.location}\n")

    content.append(f"Participants: ", style="bold cyan")
    content.append(f"{event.attendees} personne(s)\n")

    if event.notes:
        content.append(f"\nNotes: ", style="bold cyan")
        content.append(f"{event.notes}")

    panel = Panel(
        content,
        title=f"[bold magenta] {event.name}[/bold magenta]",
        border_style="white",
        box=box.ROUNDED,
        expand=False
    )

    console.print(panel)

def _display_data_list(events: List[Event], list_filter: EventFilter):
    """
    Display events table
    """
    filtre = list_filter.name if list_filter else None
    table = Table(
        title=f"[bold magenta] Liste des Événements - filtre: {filtre}[/bold magenta]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="white"
    )

    table.add_column("ID", style="dim", width=6, justify="right")
    table.add_column("Nom", style="bold", min_width=20)
    table.add_column("Début", width=16)
    table.add_column("Fin", width=16)
    table.add_column("Lieu", min_width=15)
    table.add_column("Participants", width=12, justify="right")
    table.add_column("Support", width=8, justify="center")

    for event in events:

        support = f"#{event.support_contact_id}" if event.support_contact_id else Text("-", style="dim")

        table.add_row(
            str(event.id or "-"),
            event.name,
            event.start_date.strftime("%d/%m/%Y %H:%M"),
            event.end_date.strftime("%d/%m/%Y %H:%M"),
            event.location,
            str(event.attendees),
            support
        )
    console.print(f"\nTotal: [dim]{len(events)} événement(s)[/dim]")
    console.print(table)
