from typing import Optional

import typer
from rich.console import Console

from src.domain.entities.entities import Contrat
from src.domain.entities.enums import Role, ContractStatus
from src.domain.entities.value_objects import Money
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyContratRepository
from src.use_cases.contrat_use_cases import CreateContratRequest, CreateContratUseCase, UpdateContratRequest, \
    UpdateContratUseCase, GetContratRequest, GetContratUseCase, ListContratUseCase, SignContratRequest, \
    SignContratUseCase, RecordPaymentContratRequest, RecordPaymentContratUseCase

contrat_app = typer.Typer()
console = Console()

@contrat_app.callback()
def permission(ctx:typer.Context):
    if ctx.invoked_subcommand not in ['show', "list"]:
        if ctx.obj["current_user"]["user_role"] != Role.GESTION:
            console.print("[red]Vous êtes pas authorisé à utiliser cette commande[/red]")
            raise typer.Exit()

@contrat_app.command(help="Créer un contrat")
def create(
        ctx: typer.Context,
        client_id : int = typer.Option(..., prompt=True),
        commercial_contact_id: int = typer.Option(..., prompt=True),
        contrat_amount: int = typer.Option(..., prompt=True),
):

    repo = SQLAlchemyContratRepository(ctx.obj["session"])

    request = CreateContratRequest(
        client_id,
        commercial_contact_id,
        contrat_amount =  Money(contrat_amount),
        current_user =  ctx.obj["current_user"]
    )
    use_case = CreateContratUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Client #{response.contrat.id} créé[/bold]")
    _display_data(response.contrat)

@contrat_app.command(help="Modifier un contrat")
def update(
        ctx: typer.Context,
        contrat_id: int,
           contrat_amount: Optional[int] = typer.Option(0, prompt=True, show_default=False),
           status: Optional[ContractStatus] = typer.Option('', prompt=True, show_default=False),
           ):

    def normalize(value: str | None) -> str | None:
        return value if value not in ('', 0) else None

    contrat_amount = normalize(contrat_amount)
    status = normalize(status)


    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    request = UpdateContratRequest(
        contrat_id=contrat_id,
        contrat_amount = contrat_amount ,
        status = status,
        current_user=ctx.obj["current_user"]
    )
    use_case = UpdateContratUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Client #{response.contrat.id} modifié[/bold]")
    _display_data(response.contrat)


@contrat_app.command(help="Afficher un contrat")
def show(ctx: typer.Context, contrat_id: int):

    repo = SQLAlchemyContratRepository(ctx.obj["session"])

    request = GetContratRequest(
        contrat_id=contrat_id,
        current_user= ctx.obj["current_user"]
    )
    use_case = GetContratUseCase(repo)
    response = use_case.execute(request)


    console.print(f"\n[bold]Client #{response.contrat.id}[/bold]")
    _display_data(response.contrat)

@contrat_app.command(help="Afficher tous les contrats")
def list(ctx: typer.Context):
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    use_case = ListContratUseCase(repo)

    response = use_case.execute()

    for contrat in response.contrats:
        console.print(f"\n[bold]Client #{contrat.id}[/bold]")
        _display_data(contrat)

@contrat_app.command(help="Signer un contrat")
def sign(ctx: typer.Context ,contrat_id: int):
    repo = SQLAlchemyContratRepository(ctx.obj["session"])
    request = SignContratRequest(
        contrat_id=contrat_id,
        current_user=ctx.obj["current_user"]
    )
    use_case = SignContratUseCase(repo)
    response = use_case.execute(request)

    console.print(f"Contrat #{response.contrat.id} - statut: {response.contrat.status.name} ")

@contrat_app.command(help="Effectuer un paiement")
def pay(ctx : typer.Context, contrat_id: int):
    repo = SQLAlchemyContratRepository(ctx.obj["session"])

    payment: int = typer.prompt("montant du paiment:", default=0)

    request = RecordPaymentContratRequest(
        contrat_id=contrat_id,
        payment = payment,
        current_user=ctx.obj["current_user"]
    )
    use_case = RecordPaymentContratUseCase(repo)
    response = use_case.execute(request)

    console.print(f"Contrat #{response.contrat.id} ")
    console.print(f"Montant du paiement: {payment}")
    console.print(f"Montant restant: {response.contrat.balance_due.amount}")

def _display_data(data: Contrat):

    console.print(f"  Client: ID {data.client_id}")
    console.print(f"  Commercial: ID {data.commercial_contact_id}")
    console.print(f"  Montant: {data.contrat_amount}")
    console.print(f"  Solde: {data.balance_due}")
    console.print(f"  Statut: {data.status.name}")
    console.print(f"  Créé le: {data.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {data.updated_at.strftime('%d/%m/%Y %H:%M')}\n")