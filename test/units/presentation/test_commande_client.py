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
            "user_current_id": 132,
            "user_current_role": Role.COMMERCIAL,
        },

    }


def test_client_create(make_context):
    result = runner.invoke(
        app, ['client','create'],
        input=(
            "Jean Dupont\n"
            "jean@test.com\n"
            "0600000000\n"
            "ACME\n"
        ),
        obj=make_context,

    )
    assert "créé" in result.output
    assert result.exit_code == 0

def test_client_create_invalid(make_context):
    result = runner.invoke(
        app, ['client','create'],
        input=(
            "Jean Dupont\n"
            "456465\n"
            "06000\n"
            "ACME\n"
        ),
        obj=make_context,

    )
    assert "E-mail invalide" in result.output
    assert result.exit_code == 0

def test_client_update(make_context):
    result = runner.invoke(
        app, ['client','update', '165'],
        input=(
            "New Name\n"
            "\n"
            "\n"
            "\n"
        ),
        obj=make_context,
    )

    assert "modifié" in result.output
    assert result.exit_code == 0

def test_client_show(make_context):
    result = runner.invoke(app, ['client', "show", "1"], obj=make_context)
    assert "ID" in result.output
    assert result.exit_code == 0

def test_client_show_invalid_id(make_context):
    result = runner.invoke(app,
                           ['client', "show", "1856"],
                           obj=make_context,)
    assert "Client non trouvé" in result.output
    assert result.exit_code == 0

def test_client_list(make_context):
    result = runner.invoke(app, ['client', "list"], obj=make_context)
    assert "Clients" in result.output
    assert result.exit_code == 0

def test_client_list_filter_invalid(make_context):
    result = runner.invoke(app, ['client', "list", "-f", "invalid"], obj=make_context)
    assert "Invalid value" in result.output
    assert result.exit_code == 2

def test_client_list_filter_valid(make_context):
    result = runner.invoke(app, ['client', "list", "-f", "mine"], obj=make_context)
    assert "Clients" in result.output
    assert result.exit_code == 0

def test_client_delete_invalid():
    contexte= {
        "current_user": {
            "user_current_id": 132,
            "user_current_role": Role.ADMIN,
        },
    }

    result = runner.invoke(app, ['client', "delete", "5459"], obj=contexte)
    assert "Client non trouvé" in result.output
    assert result.exit_code == 0

def test_client_delete_valid():
    context= {
        "current_user": {
            "user_current_id": 132,
            "user_current_role": Role.ADMIN,
        },
    }

    create_result = runner.invoke(
        app,
        ['client', "create"],
        input=(
            "Jean Dupont\n"
            "jean@todelete.fr\n"
            "0600000000\n"
            "ACME\n"
            ),
        obj=context
    )

    match = re.search(r"Client\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout

    client_id = match.group(1)

    delete_result = runner.invoke(app, ['client', "delete", client_id], input="y", obj=context)

    assert f"Client #{client_id} supprimé" in delete_result.stdout
    assert delete_result.exit_code == 0
