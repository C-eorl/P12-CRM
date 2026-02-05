import typer
from rich.console import Console

from helpers.helpers import get_current_user
from src.infrastructures.database.session import get_session
from src.infrastructures.security.security import TokenStore
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
            console.print("[red]Veuillez vous connecter via - auth login -[/red]")
            raise typer.Exit(1)


