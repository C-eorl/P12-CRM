import typer

from src.presentation.cli.commands.auth_commands import auth_app
from src.presentation.cli.commands.client_commands import client_app
from src.presentation.cli.commands.contrat_commands import contrat_app
from src.presentation.cli.commands.event_commands import event_app
from src.presentation.cli.commands.user_commands import user_app

app = typer.Typer()

app.add_typer(auth_app, name="auth", help="Authentification")
app.add_typer(user_app, name="user", help="Commandes liées aux utilisateurs")
app.add_typer(client_app, name="client", help="Commandes liées aux clients")
app.add_typer(contrat_app, name="contrat", help="Commandes liées aux contrats")
app.add_typer(event_app, name="event", help="Commandes liées aux évènements")
