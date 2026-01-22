
import typer
from rich.console import Console
from sqlalchemy.orm import Session

from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email
from src.infrastructures.database.session import get_session
from src.infrastructures.repositories.SQLAchemy_repository import SQLAchemyClientRepository
from src.use_cases.client_use_cases import GetClientUseCase, GetClientRequest

client_app = typer.Typer()
console = Console()

@client_app.command()
def create():
    typer.echo("Creating new client")

@client_app.command()
def show(client_id: int):


    session = get_session()
    repo = SQLAchemyClientRepository(session)

    request = GetClientRequest(
        client_id=client_id,
        current_user= User(
            id=5,
            full_name="test test",
            email=Email("test@test.com"), password="sfsefs",
            role=Role.COMMERCIAL
        )
    )
    use_case = GetClientUseCase(repo)
    response = use_case.execute(request)

    console.print(f"\n[bold]Client #{response.user.id}[/bold]")
    console.print(f"  Nom: {response.user_id.fullname}")
    console.print(f"  Email: {response.user.email}")
    console.print(f"  Téléphone: {response.user.telephone}")
    console.print(f"  Entreprise: {response.user.company_name}")
    console.print(f"  Commercial: ID {response.user.commercial_contact_id}")
    console.print(f"  Créé le: {response.user.created_at.strftime('%d/%m/%Y %H:%M')}")
    console.print(f"  Mis à jour: {response.user_id.updated_at.strftime('%d/%m/%Y %H:%M')}\n")