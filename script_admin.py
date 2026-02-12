import typer
from rich.console import Console

from src.domain.entities.entities import User
from src.domain.entities.enums import Role
from src.domain.entities.value_objects import Email
from src.infrastructures.database.session import get_session
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import BcryptPasswordHasher


from dotenv import load_dotenv
load_dotenv()
console = Console()

def create_admin():
    console.print("\n[bold cyan]═══ Création du premier utilisateur admin ═══[/bold cyan]\n")

    fullname = typer.prompt('Nom complet', type=str)
    email = typer.prompt('Email', type=str)
    password = typer.prompt('Mot de passe', type=str)
    password_confirm = typer.prompt('Confirmez le mot de passe', type=str)

    if password != password_confirm:
        console.print("[red] Les mots de passe ne correspondent pas[/red]")
        return

    try:
        email = Email(email)

        hacher = BcryptPasswordHasher()
        password_hash = hacher.hash_password(password)

        admin_user = User(
            id=None,
            fullname=fullname,
            email=email,
            password=password_hash,
            role=Role.ADMIN
        )

        session = get_session()
        repo = SQLAlchemyUserRepository(session)
        if repo.find_by_email(email.address):
            console.print(f"[red] Un utilisateur avec l'email {email} existe déjà[/red]")
            return

        saved_user = repo.save(admin_user)

        console.print(f"\n[green] Utilisateur admin créé avec succès![/green]")
        console.print(f"  ID: {saved_user.id}")
        console.print(f"  Nom: {saved_user.fullname}")
        console.print(f"  Email: {saved_user.email}")
        console.print(f"  Rôle: {saved_user.role}\n")

        console.print("[cyan]Vous pouvez maintenant vous connecter avec:[/cyan]")
        console.print(f"  python main.py auth login\n")

        session.close()
    except Exception as e:
        console.print(f"[red] Erreur lors de la création: {str(e)}[/red]")

if __name__ == "__main__":
    create_admin()