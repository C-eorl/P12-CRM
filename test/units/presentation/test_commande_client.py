import re

from typer.testing import CliRunner

from src.presentation.cli.cli_main import app

runner = CliRunner()


def test_client_create():
    result = runner.invoke(
        app, ['client','create'],
        input=(
            "Jean Dupont\n"
            "jean@test.com\n"
            "0600000000\n"
            "ACME\n"
        ),

    )
    assert "créé" in result.output
    assert result.exit_code == 0

def test_client_create_invalid():
    result = runner.invoke(
        app, ['client','create'],
        input=(
            "Jean Dupont\n"
            "456465\n"
            "06000\n"
            "ACME\n"
        ),

    )
    assert "Erreur" in result.output
    assert result.exit_code == 0

def test_client_update():
    result = runner.invoke(
        app, ['client','update', '1'],
        input=(
            "New Name\n"
            "\n"
            "\n"
            "\n"
        )
    )

    assert result.exit_code == 0
    assert "modifié" in result.output

def test_client_show():
    result = runner.invoke(app, ['client', "show", "1"])
    assert "ID" in result.output
    assert result.exit_code == 0

def test_client_show_invalid_id():
    result = runner.invoke(app, ['client', "show", "1856"])
    assert "Client non trouvé" in result.output
    assert result.exit_code == 0

def test_client_list():
    result = runner.invoke(app, ['client', "list"])
    assert "Clients" in result.output
    assert result.exit_code == 0

def test_client_list_filter_invalid():
    result = runner.invoke(app, ['client', "list", "-f", "invalid"])
    assert "Invalid value" in result.output
    assert result.exit_code == 2

def test_client_list_filter_valid():
    result = runner.invoke(app, ['client', "list", "-f", "mine"])
    assert "Clients" in result.output
    assert result.exit_code == 0

def test_client_delete_invalid():
    result = runner.invoke(app, ['client', "delete", "1456"])
    assert "Client non trouvé" in result.output
    assert result.exit_code == 0

def test_client_delete_valid():
    create_result = runner.invoke(
        app,
        ['client', "create"],
        input=(
            "Jean Dupont\n"
            "jean@todelete.fr\n"
            "0600000000\n"
            "ACME\n"
            )
    )

    match = re.search(r"Client\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout

    client_id = match.group(1)

    delete_result = runner.invoke(app, ['client', "delete", client_id])

    assert delete_result.exit_code == 0
    assert f"Client #{client_id} supprimé" in delete_result.stdout