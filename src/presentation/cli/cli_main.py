import os

import typer
from dotenv import set_key, load_dotenv
from rich.console import Console
from sentry_sdk import set_user

from helpers.helper_cli import error_display
from helpers.helpers import get_current_user
from src.infrastructures.database.session import get_session, init_db, init_postgresql
from src.presentation.cli.commands.auth_commands import auth_app
from src.presentation.cli.commands.client_commands import client_app
from src.presentation.cli.commands.contrat_commands import contrat_app
from src.presentation.cli.commands.event_commands import event_app
from src.presentation.cli.commands.user_commands import user_app

app = typer.Typer()
console = Console()

app.add_typer(auth_app, name="auth", help="Authentification")
app.add_typer(user_app, name="user", help="Commandes liées aux utilisateurs")
app.add_typer(client_app, name="client", help="Commandes liées aux clients")
app.add_typer(contrat_app, name="contrat", help="Commandes liées aux contrats")
app.add_typer(event_app, name="event", help="Commandes liées aux évènements")




@app.callback()
def main(ctx: typer.Context):
    """
    Callback auth verification before command
    Initialisation Context and add session(DB), current_user(dict)
    """

    ctx.ensure_object(dict)
    ctx.obj["session"] = get_session()
    ctx.obj["current_user"] = get_current_user()


    if ctx.obj["current_user"] is None:

        if ctx.invoked_subcommand not in ["auth", "init"]:
            error_display("Erreur Authentification", "Veuillez vous connecter via - auth login -")
            raise typer.Exit(1)
        if ctx.invoked_subcommand in ["auth", "init"]:
            pass

    if ctx.obj["current_user"] is not None:
        set_user({
            "id": ctx.obj["current_user"]["user_current_id"],
            "role": ctx.obj["current_user"]["user_current_role"].value
        })
    ctx.call_on_close(ctx.obj["session"].close)

@app.command()
def init():
    """Command initialize database"""
    console.print("Veuillez vous connecter à votre Base de donnée via nos identifiant")
    user = typer.prompt("Utilisateur", default="postgres")
    password = typer.prompt("Mot de passe", default="")
    db_name = typer.prompt("Nom de la base de donnée que vous allez créer")

    try:
        result = init_postgresql(user, password, db_name)
        if not result:
            error_display("Existant", f"La base de donnée {db_name} existe déjà")
            raise typer.Exit()
        else:
            console.print(f"[green]* Base de données {db_name} avec succès[/green]")

        database_url = f"postgresql+psycopg2://{user}:{password}@localhost/{db_name}"
        set_key(".env","DATABASE_URL",database_url)
        os.environ["DATABASE_URL"] = database_url

        console.print("[yellow]* Initialisation de la base de données...[/yellow]")
        init_db()
        console.print("[green]* Base de données initialisée avec succès![/green]")

    except Exception as e:
        console.print(f"[red] Erreur lors de l'initialisation: {str(e)}[/red]")