import typer

from src.infrastructures.database.session import get_session
from src.infrastructures.repositories.SQLAchemy_repository import SQLAlchemyUserRepository
from src.infrastructures.security.security import TokenStore, JWTTokenManager
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


def get_current_user() :
    token = TokenStore.get_token()
    if token is None:
        return None

    jwt = JWTTokenManager()
    payload = jwt.decode_token(token)
    if payload is None:
        return None
    repo = SQLAlchemyUserRepository(get_session())
    user = repo.find_by_id(payload["user_id"])
    return {"user_id": user.id, "user_role": user.role}

@app.callback()
def main(ctx: typer.Context):
    ctx.ensure_object(dict)

    ctx.obj["session"] = get_session()
    ctx.obj["current_user"] = get_current_user()

    token = TokenStore.has_token()
    if ctx.invoked_subcommand != "auth":
        if not token:
            typer.echo("Veuillez vous connecter via - auth login -")
            raise typer.Exit(1)

    if ctx.invoked_subcommand == "auth":
        if token:
            typer.echo("Vous êtes déjà connecté")
            raise typer.Exit(1)