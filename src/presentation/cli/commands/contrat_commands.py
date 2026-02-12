from typing import Optional, List

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from helpers.helper_cli import error_display
from helpers.helpers import normalize
from src.domain.entities.entities import Contrat
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Money
from src.domain.policies.user_policy import RequestPolicy, UserPolicy
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyContratRepository, \
    SQLAlchemyClientRepository, SQLAlchemyUserRepository
from src.use_cases.contrat_use_cases import CreateContratRequest, CreateContratUseCase, UpdateContratRequest, \
    UpdateContratUseCase, GetContratRequest, GetContratUseCase, ListContratUseCase, SignContratRequest, \
    SignContratUseCase, RecordPaymentContratRequest, RecordPaymentContratUseCase, ContratFilter, ListContratRequest, \
    DeleteContratUseCase, DeleteContratRequest, UpdateContratResponse

contrat_app = typer.Typer()
console = Console()

@contrat_app.callback()
def permission(ctx:typer.Context):
    """Callback - verify user role """
    ctx.obj["ressource"] = "CONTRAT"

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

@contrat_app.command(help="Créer un contrat")
def create(
        ctx: typer.Context,
        client_id : int = typer.Option(..., prompt=True),
        commercial_contact_id: int = typer.Option(..., prompt=True),
        contrat_amount: int = typer.Option(..., prompt=True),
):
    """
    Command for creation client
    :param ctx: typer Context
    :param client_id: ID client linked to the contrat
    :param commercial_contact_id: ID commercial contact linked to the contrat
    :param contrat_amount: amount of the contrat
    :return: None
    """
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    client_repo = SQLAlchemyClientRepository(ctx.obj["session"])
    user_repo = SQLAlchemyUserRepository(ctx.obj["session"])

    if not client_repo.exist(client_id):
        error_display("Ressource", "Client non trouvé")
        raise typer.Exit(1)

    if not user_repo.exist(commercial_contact_id) :
        error_display("Ressource", "Utilisateur non trouvé")
        raise typer.Exit(1)

    user_commercial = user_repo.find_by_id(commercial_contact_id)
    if not user_commercial.is_commercial():
        error_display("Ressource", "L'utilisateur selectionné n'est pas du département commercial")
        raise typer.Exit(1)
    use_case = CreateContratUseCase(repo)

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="create"
    )

    request = CreateContratRequest(
        client_id= client_id,
        commercial_contact_id= commercial_contact_id,
        contrat_amount =  Money(contrat_amount),
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Contrat #{response.contrat.id} créé[/bold]\n")
        _display_data(response.contrat)
    else:
        error_display(response.error, response.msg)


@contrat_app.command(help="Modifier un contrat")
def update(ctx: typer.Context,contrat_id: int):
    """
    Command for update contrat
    :param ctx: typer Context
    :param contrat_id: ID contrat
    :return: None
    """
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = UpdateContratUseCase(repo)

    #verification ressource existe
    contrat = repo.find_by_id(contrat_id)
    if not contrat:
        error_display("Ressource", "Contrat non trouvé")
        raise typer.Exit()

    if contrat.has_sign():
            error_display("Erreur Métier", "Aucune modification permise sur un contrat signé")
            raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="update"
    )

    contrat_amount = typer.prompt("Montant du contrat", default=0, show_default=False)

    contrat_amount = normalize(contrat_amount)

    request = UpdateContratRequest(
        contrat_id=contrat_id,
        contrat_amount = Money(contrat_amount),
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Contrat #{response.contrat.id} modifié[/bold]\n")
        _display_data(response.contrat)
    else:
        error_display(response.error, response.msg)


@contrat_app.command(help="Afficher un contrat")
def show(ctx: typer.Context, contrat_id: int):
    """
    Command for show contrat
    :param ctx: typer Context
    :param contrat_id: ID contrat
    :return: None
    """
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = GetContratUseCase(repo)

    if not repo.exist(contrat_id):
        error_display("Ressource", "Contrat non trouvé")
        raise typer.Exit()

    request = GetContratRequest(
        contrat_id=contrat_id
    )
    response = use_case.execute(request)

    if response.success:
        _display_data(response.contrat)
    else:
        error_display(response.error, response.msg)

@contrat_app.command(help="Afficher tous les contrats")
def list(
        ctx: typer.Context,
        list_filter: Optional[ContratFilter] = typer.Option(
            None, "--filter", "-f",
        help="Filter contrat",
        )
):
    """
    Command for list contrats
    :param list_filter: filter contrat
    :param ctx: typer Context
    :return: None
    """
    request = ListContratRequest(
        commercial_contact_id = ctx.obj["current_user"]["user_current_id"],
        list_filter = list_filter
    )
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = ListContratUseCase(repo)
    response = use_case.execute(request)

    if response.success:
            _display_data_list(response.contrats, list_filter)
    else:
        error_display(response.error, response.msg)

@contrat_app.command(help="Signer un contrat")
def sign(ctx: typer.Context ,contrat_id: int):
    """
    Command for sign contrat
    :param ctx: typer Context
    :param contrat_id: ID contrat
    :return: None
    """
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = SignContratUseCase(repo)

    if not repo.exist(contrat_id):
        error_display("Ressource", "Contrat non trouvé")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="sign"
    )

    request = SignContratRequest(
        contrat_id=contrat_id,
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"Contrat #{response.contrat.id} - statut: {response.contrat.status.name} ")
    else:
        error_display(response.error, response.msg)

@contrat_app.command(help="Effectuer un paiement")
def pay(ctx : typer.Context, contrat_id: int):
    """
    Command for pay contrat
    :param ctx: typer Context
    :param contrat_id: ID contrat
    :return: None
    """
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = RecordPaymentContratUseCase(repo)

    contrat = repo.find_by_id(contrat_id)
    if not contrat:
        error_display("Ressource", "Contrat non trouvé")
        raise typer.Exit()

    if contrat.has_sign():
        error_display("Erreur Métier", "La signature du contrat est nécessaire")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="pay"
    )

    payment: int = typer.prompt("montant du paiement", default=0, show_default=False)

    request = RecordPaymentContratRequest(
        contrat_id=contrat_id,
        payment = payment,
        authorization=policy
    )
    response = use_case.execute(request)

    if response.success:
        console.print(f"Contrat #{response.contrat.id} ")
        console.print(f"Montant du paiement: {payment}")
        console.print(f"Montant restant: {response.contrat.balance_due.amount}")
        console.print(f"Montant total: {response.contrat.contrat_amount.amount}")
    else:
        error_display(response.error, response.msg)

@contrat_app.command(help="Supprimer un contrat")
def delete(ctx: typer.Context, contrat_id: int):
    """
    Command for delete contrat
    :param ctx: typer Context
    :param contrat_id: ID of contrat
    :return: None
    """
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = DeleteContratUseCase(repo)

    #verification ressource existe
    if not repo.exist(contrat_id):
        error_display("Ressource", "Contrat non trouvé")
        raise typer.Exit()

    if not typer.confirm(f"Etes-vous sure de vouloir supprimer le Contrat #{contrat_id} ?"):
        error_display("Annulation", "Suppression du contrat annulé")
        raise typer.Exit()

    policy = RequestPolicy(
        user=ctx.obj["current_user"],
        ressource=ctx.obj["ressource"],
        action="delete"
    )
    request = DeleteContratRequest(
        contrat_id=contrat_id,
        authorization= policy,
    )

    response = use_case.execute(request)

    if response.success:
        console.print(f"\n[bold]Contrat #{contrat_id} supprimé[/bold]")
    else:
        error_display(response.error, response.msg)

def _display_data(contrat: Contrat):
    """ Display data of Contrat """

    content = Text()

    content.append(f"\nID: ", style="bold cyan")
    content.append(f"{contrat.id or 'N/A'}\n")

    content.append(f"Client: ", style="bold cyan")
    content.append(f"{contrat.client_id}\n")

    content.append(f"Contact commercial: ", style="bold cyan")
    content.append(f"{contrat.commercial_contact_id}\n")

    content.append(f"Montant du contrat: ", style="bold cyan")
    content.append(f"{contrat.contrat_amount}\n")

    content.append(f"Somme restante: ", style="bold cyan")
    content.append(f"{contrat.balance_due}\n")

    content.append(f"Status: ", style="bold cyan")
    content.append(f"{contrat.status.name}\n")

    panel = Panel(
        content,
        title=f"[bold magenta] Contrat #{contrat.id}[/bold magenta]",
        border_style="white",
        box=box.ROUNDED,
        expand=False
    )

    console.print(panel)

def _display_data_list(contrats: List[Contrat], list_filter: ContratFilter):
    """
    Display contrats table
    """
    filtre = list_filter.name if list_filter else None
    table = Table(
        title=f"[bold magenta] Liste des Contrats - filtre: {filtre}[/bold magenta]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="white"
    )

    table.add_column("ID", style="dim", width=6, justify="right")
    table.add_column("Client", style="bold", min_width=20)
    table.add_column("Contact commercial", width=16)
    table.add_column("Montant du contrat", width=16)
    table.add_column("Somme restante", min_width=15)
    table.add_column("Status", width=12, justify="right")

    for contrat in contrats:

        table.add_row(
            str(contrat.id or "-"),
            str(contrat.client_id),
            str(contrat.commercial_contact_id),
            str(contrat.contrat_amount),
            str(contrat.balance_due),
            contrat.status.name
        )
    console.print(f"\nTotal: [dim]{len(contrats)} contrat(s)[/dim]")
    console.print(table)