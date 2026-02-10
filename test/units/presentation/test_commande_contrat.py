import re

from typer.testing import CliRunner

from src.presentation.cli.cli_main import app

runner = CliRunner()


def test_contrat_create():
    result = runner.invoke(
        app, ['contrat','create'],
        input=(
            "3\n"
            "4\n"
            "500\n"
        ),
    )
    assert "créé" in result.output
    assert result.exit_code == 0

def test_contrat_create_invalid_client_id():
    result = runner.invoke(
        app, ['contrat', 'create'],
        input=(
            "4\n"
            "2\n"
            "500\n"
        ),
    )
    assert "Client non trouvé" in result.output
    assert result.exit_code == 1

def test_contrat_create_invalid_user_id():
    result = runner.invoke(
        app, ['contrat', 'create'],
        input=(
            "3\n"
            "1565\n"
            "500\n"
        ),
    )
    assert "Utilisateur non trouvé" in result.output
    assert result.exit_code == 1

def test_contrat_create_not_contact_commercial():
    result = runner.invoke(
        app, ['contrat', 'create'],
        input=(
            "3\n"
            "1\n"
            "500\n"
        ),
    )
    assert "n'est pas du département commercial" in result.output
    assert result.exit_code == 1

def test_contrat_update():
    result = runner.invoke(
        app, ['contrat','update', '1'],
        input=(
            "10000"
        )
    )

    assert result.exit_code == 0
    assert "modifié" in result.output

def test_contrat_update_invalid():
    result = runner.invoke(
        app, ['contrat','update', '1'],
        input=(
            "fdf"
        )
    )

    assert result.exit_code == 1
    assert "is not a valid integer" in result.output

def test_contrat_show():
    result = runner.invoke(app, ['contrat', "show", "1"])
    assert "ID" in result.output
    assert result.exit_code == 0

def test_contrat_show_invalid_id():
    result = runner.invoke(app, ['contrat', "show", "4156"])
    assert "Contrat non trouvé" in result.output
    assert result.exit_code == 0

def test_contrat_list():
    result = runner.invoke(app, ['contrat', "list"])
    assert "Contrats" in result.output
    assert result.exit_code == 0

def test_contrat_list_filter_invalid():
    result = runner.invoke(app, ['contrat', "list", "-f", "invalid"])
    assert "Invalid value" in result.output
    assert result.exit_code == 2

def test_contrat_list_filter_valid():
    result = runner.invoke(app, ['contrat', "list", "-f", "signed"])
    assert "Contrats" in result.output
    assert result.exit_code == 0

def test_contrat_delete_invalid():
    result = runner.invoke(app, ['contrat', "delete", "1456"])
    assert "Contrat non trouvé" in result.output
    assert result.exit_code == 0

def test_contrat_delete_valid():
    create_result = runner.invoke(
        app, ['contrat','create'],
        input=(
            "3\n"
            "4\n"
            "500\n"
        ),
    )

    match = re.search(r"Contrat\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout

    client_id = match.group(1)

    delete_result = runner.invoke(app, ['contrat', "delete", client_id])

    assert delete_result.exit_code == 0
    assert f"Contrat #{client_id} supprimé" in delete_result.stdout