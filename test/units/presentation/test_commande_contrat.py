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

def test_contrat_create(make_context):
    result = runner.invoke(
        app, ['contrat','create'],
        input=(
            "3\n"
            "4\n"
            "500\n"
        ),
        obj=make_context
    )
    assert "créé" in result.output
    assert result.exit_code == 0

def test_contrat_create_invalid_client_id(make_context):
    result = runner.invoke(
        app, ['contrat', 'create'],
        input=(
            "4\n"
            "2\n"
            "500\n"
        ),
        obj=make_context
    )
    assert "Client non trouvé" in result.output
    assert result.exit_code == 1

def test_contrat_create_invalid_user_id(make_context):
    result = runner.invoke(
        app, ['contrat', 'create'],
        input=(
            "3\n"
            "1565\n"
            "500\n"
        ),
        obj=make_context
    )
    assert "Utilisateur non trouvé" in result.output
    assert result.exit_code == 1

def test_contrat_create_not_contact_commercial(make_context):
    result = runner.invoke(
        app, ['contrat', 'create'],
        input=(
            "165\n"
            "134\n"
            "500\n"
        ),
        obj=make_context
    )
    assert "n'est pas du département commercial" in result.output
    assert result.exit_code == 1

def test_contrat_update(make_context):
    result = runner.invoke(
        app, ['contrat','update', '98'],
        input=(
            "10000"
        ),
        obj=make_context
    )

    assert result.exit_code == 0
    assert "modifié" in result.output

def test_contrat_update_invalid(make_context):
    result = runner.invoke(
        app, ['contrat','update', '1'],
        input=(
            "fdf"
        ),
        obj=make_context
    )

    assert result.exit_code == 1
    assert "is not a valid integer" in result.output

def test_contrat_show(make_context):
    result = runner.invoke(app, ['contrat', "show", "1"],obj=make_context)
    assert "ID" in result.output
    assert result.exit_code == 0

def test_contrat_show_invalid_id(make_context):
    result = runner.invoke(app, ['contrat', "show", "4156"],obj=make_context)
    assert "Contrat non trouvé" in result.output
    assert result.exit_code == 0

def test_contrat_list(make_context):
    result = runner.invoke(app, ['contrat', "list"],obj=make_context)
    assert "Contrats" in result.output
    assert result.exit_code == 0

def test_contrat_list_filter_invalid(make_context):
    result = runner.invoke(app, ['contrat', "list", "-f", "invalid"],obj=make_context)
    assert "Invalid value" in result.output
    assert result.exit_code == 2

def test_contrat_list_filter_valid(make_context):
    result = runner.invoke(app, ['contrat', "list", "-f", "signed"],obj=make_context)
    assert "Contrats" in result.output
    assert result.exit_code == 0

def test_contrat_delete_invalid(make_context):
    result = runner.invoke(
        app,
        ['contrat', "delete", "1456"],
        obj={
            "current_user": {
                "user_current_id": 133,
                "user_current_role": Role.ADMIN,
            },
        }
    )
    assert "Contrat non trouvé" in result.output
    assert result.exit_code == 0

def test_contrat_delete_valid(make_context):
    create_result = runner.invoke(
        app, ['contrat','create'],
        input=(
            "3\n"
            "4\n"
            "500\n"
        ),
        obj=make_context
    )

    match = re.search(r"Contrat\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout

    client_id = match.group(1)

    delete_result = runner.invoke(
        app,
        ['contrat', "delete", client_id],
        obj={
        "current_user": {
            "user_current_id": 133,
            "user_current_role": Role.ADMIN,
        },
    },
        input="y"
    )

    assert f"Contrat #{client_id} supprimé" in delete_result.stdout
    assert delete_result.exit_code == 0
