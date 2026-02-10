import re
from typer.testing import CliRunner

from src.presentation.cli.cli_main import app

runner = CliRunner()


def test_user_create():
    result = runner.invoke(
        app, ["user", "create"],
        input=(
            "Jean Support\n"
            "support@test.fr\n"
            "password123\n"
            "SUPPORT\n"
        ),
    )

    assert result.exit_code == 0
    assert "créé" in result.output


def test_user_create_invalid_role():
    result = runner.invoke(
        app, ["user", "create"],
        input=(
            "Jean\n"
            "test@test.fr\n"
            "password\n"
            "INVALID\n"
        ),
    )

    assert "Role (COMMERCIAL, SUPPORT, GESTION, ADMIN)" in result.output
    assert result.exit_code == 1


def test_user_update():
    result = runner.invoke(
        app, ["user", "update", "130"],
        input=(
            "Jean Modifié\n"
            "modifie@test.fr\n"
        ),
    )

    assert "modifié" in result.output
    assert result.exit_code == 0


def test_user_update_invalid():
    result = runner.invoke(app, ["user", "update", "9999"])
    assert result.exit_code == 0
    assert "Utilisateur non trouvé" in result.output


def test_user_show():
    result = runner.invoke(app, ["user", "show", "1"])
    assert result.exit_code == 0
    assert "Utilisateur #" in result.output


def test_user_show_invalid():
    result = runner.invoke(app, ["user", "show", "9999"])
    assert result.exit_code == 0
    assert "non trouvé" in result.output.lower()


def test_user_list():
    result = runner.invoke(app, ["user", "list"])
    assert result.exit_code == 0
    assert "Utilisateurs" in result.output


def test_user_list_filter_invalid():
    result = runner.invoke(app, ["user", "list", "-f", "invalid"])
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_user_list_filter_valid():
    result = runner.invoke(app, ["user", "list", "-f", "role:support"])
    assert result.exit_code == 0


def test_user_delete_valid():
    create_result = runner.invoke(
        app, ["user", "create"],
        input=(
            "Temp User\n"
            "temp@test.fr\n"
            "password\n"
            "SUPPORT\n"
        ),
    )

    match = re.search(r"Utilisateur\s+#(\d+)\s+créé", create_result.output)
    assert match

    user_id = match.group(1)

    delete_result = runner.invoke(app, ["user", "delete", user_id])

    assert delete_result.exit_code == 0
    assert f"Utilisateur #{user_id} supprimé" in delete_result.output


def test_user_delete_invalid():
    result = runner.invoke(app, ["user", "delete", "9999"])
    assert result.exit_code == 0
    assert "Utilisateur non trouvé" in result.output
