import typer
from rich.console import Console
from sentry_sdk import set_user

from helpers.helper_cli import error_display
from helpers.helpers import get_current_user
from src.infrastructures.database.session import get_session, init_db
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
        if ctx.invoked_subcommand == "auth":
            pass
        if ctx.invoked_subcommand != "auth":
            error_display("Erreur Authentification", "Veuillez vous connecter via - auth login -")
            raise typer.Exit(1)

    if ctx.obj["current_user"] is not None:
        set_user({
            "id": ctx.obj["current_user"]["user_current_id"],
            "role": ctx.obj["current_user"]["user_current_role"].value
        })
    ctx.call_on_close(ctx.obj["session"].close)

@app.command()
def init():
    """Command initialize database"""
    try:
        console.print("[yellow]Initialisation de la base de données...[/yellow]")
        init_db()
        console.print("[green]* Base de données initialisée avec succès![/green]")
    except Exception as e:
        console.print(f"[red]✗ Erreur lors de l'initialisation: {str(e)}[/red]")