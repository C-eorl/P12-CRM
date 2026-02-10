import re

from typer.testing import CliRunner

from src.presentation.cli.cli_main import app

runner = CliRunner()

def login_as(email: str, password: str):
    logout = runner.invoke(app, ["auth", "logout"])

    result = runner.invoke(app, ["auth", "login"], input=f"{email}\n{password}\n")
    assert "connecté" in result.stdout
    return result

def test_commercial_flow():


    COMMERCIAL_ID = 132
    SUPPORT_ID = 134


    login_as("commercial@test.com", "commercial")

    #Crée un client
    client = runner.invoke(
        app, ["client", "create"],
        input=(
            "Flow integration\n"
            "integration@flow.fr\n"
            "0656545854\n"
            "Ent. flow\n"
        )
    )
    assert "créé" in client.stdout
    assert client.exit_code == 0
    match = re.search(r"Client\s+#(\d+)\s+créé", client.stdout)
    assert match, client.stdout
    client_id = match.group(1)


    login_as("gestion@test.com", "gestion")

    # Crée un contrat
    contrat = runner.invoke(
        app, ["contrat", "create"],
        input=(
            f"{client_id}\n"
            f"{COMMERCIAL_ID}\n"
            "0656545854\n"
            "Ent. flow\n"
        )
    )
    assert contrat.exit_code == 0
    assert "créé" in contrat.stdout

    match = re.search(r"Contrat\s+#(\d+)\s+créé", contrat.stdout)
    assert match, contrat.stdout
    contrat_id = match.group(1)

    login_as("commercial@test.com", "commercial")

    # signé le contrat
    sign = runner.invoke(
        app, ["contrat", "sign", f"{contrat_id}"],
    )
    assert "statut" in sign.stdout
    assert sign.exit_code == 0

    event = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            f"{COMMERCIAL_ID}\n"
            f"{client_id}\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        )
    )
    assert event.exit_code == 0
    assert "créé" in event.stdout
    match = re.search(r"Evènement\s+#(\d+)\s+créé", event.stdout)
    assert match, event.stdout
    event_id = match.group(1)

    login_as("gestion@test.com", "gestion")

    assign = runner.invoke(
        app, ["event", "assign", event_id],
        input=(
            f"{SUPPORT_ID}\n"
        )
    )
    assert "assigné à User" in assign.stdout
    assert assign.exit_code == 0

############################################################################
#           Déconnexion & connexion                                        #
############################################################################
    logout = runner.invoke(app, ["auth", "logout"])
    assert "Vous êtes déconnecté" in logout.stdout
    assert logout.exit_code == 0