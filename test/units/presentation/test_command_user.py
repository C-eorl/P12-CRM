import re

import pytest
from typer.testing import CliRunner

from src.domain.entities.enums import Role
from src.presentation.cli.cli_main import app

runner = CliRunner()


@pytest.fixture(scope='module')
def make_context():
    return {
        "current_user": {
            "user_current_id": 133,
            "user_current_role": Role.GESTION,
        },

    }

def test_user_create(make_context):
    result = runner.invoke(
        app, ["user", "create"],
        input=(
            "Jean Support\n"
            "support@test.fr\n"
            "password123\n"
            "password123\n"
            "SUPPORT\n"
        ),
        obj=make_context,
    )

    assert "créé" in result.output
    assert result.exit_code == 0


def test_user_create_invalid_role(make_context):
    result = runner.invoke(
        app, ["user", "create"],
        input=(
            "Jean\n"
            "test@test.fr\n"
            "password\n"
            "INVALID\n"
        ),
        obj=make_context,
    )

    assert "Role (COMMERCIAL, SUPPORT, GESTION, ADMIN)" in result.output
    assert result.exit_code == 1


def test_user_update(make_context):
    result = runner.invoke(
        app, ["user", "update", "110"],
        input=(
            "Jean Modifié\n"
            "modifie@test.fr\n"
        ),
        obj=make_context,
    )

    assert "modifié" in result.output
    assert result.exit_code == 0


def test_user_update_invalid(make_context):
    result = runner.invoke(
        app,
        ["user", "update", "9999"],
        obj=make_context,
    )
    assert result.exit_code == 0
    assert "Utilisateur non trouvé" in result.output


def test_user_show(make_context):
    result = runner.invoke(
        app,
        ["user", "show", "2"],
        obj=make_context,
    )
    assert result.exit_code == 0
    assert "Utilisateur #" in result.output


def test_user_show_invalid(make_context):
    result = runner.invoke(app, ["user", "show", "9999"], obj=make_context)
    assert result.exit_code == 0
    assert "non trouvé" in result.output.lower()


def test_user_list(make_context):
    result = runner.invoke(app, ["user", "list"], obj=make_context)
    assert result.exit_code == 0
    assert "Utilisateurs" in result.output


def test_user_list_filter_invalid(make_context):
    result = runner.invoke(app, ["user", "list", "-f", "invalid"], obj=make_context)
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_user_list_filter_valid(make_context):
    result = runner.invoke(app, ["user", "list", "-f", "role:support"], obj=make_context)
    assert result.exit_code == 0


def test_user_delete_valid(make_context):
    create_result = runner.invoke(
        app, ["user", "create"],
        input=(
            "Temp User\n"
            "temp@test.fr\n"
            "password\n"
            "password\n"
            "SUPPORT\n"
        ),
    obj = make_context
    )

    match = re.search(r"Utilisateur\s+#(\d+)\s+créé", create_result.output)
    assert match

    user_id = match.group(1)

    delete_result = runner.invoke(
        app,
        ["user", "delete", user_id],
        obj=make_context,
        input="y\n"
    )

    assert delete_result.exit_code == 0
    assert f"Utilisateur #{user_id} supprimé" in delete_result.output


def test_user_delete_invalid(make_context):
    result = runner.invoke(app, ["user", "delete", "9999"], obj=make_context)
    assert result.exit_code == 0
    assert "Utilisateur non trouvé" in result.output
