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

def test_event_create(make_context):
    result = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            "149\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        ),
        obj=make_context,
    )

    assert "créé" in result.output
    assert result.exit_code == 0

def test_event_update(make_context):
    result = runner.invoke(
        app, ["event", "update", "5"],
        input=(
            "Conférence modifiée\n"
            "2027-01-02 09:00:00\n"
            "2027-01-02 17:00:00\n"
            "Lyon\n"
            "150\n"
            "Nouvelles notes\n"
        ),
        obj={
        "current_user": {
            "user_current_id": 5,
            "user_current_role": Role.SUPPORT,
            },
        }
    )

    assert "modifié" in result.output
    assert result.exit_code == 0

def test_event_update_no_linked_support(make_context):
    result = runner.invoke(
        app, ["event", "update", "2"],
        input=(
            "Conférence modifiée\n"
            "2027-01-02 09:00:00\n"
            "2027-01-02 17:00:00\n"
            "Lyon\n"
            "150\n"
            "Nouvelles notes\n"
        ),
        obj={
        "current_user": {
            "user_current_id": 132,
            "user_current_role": Role.SUPPORT,
            },
        }
    )

    assert "Permission" in result.output
    assert result.exit_code == 1


def test_event_update_invalid_id():
    result = runner.invoke(
        app,
        ["event", "update", "9999"],
        obj={
            "current_user": {
                "user_current_id": 132,
                "user_current_role": Role.SUPPORT,
            },
        }
    )

    assert result.exit_code == 1
    assert "Evènement non trouvé" in result.output


def test_event_show(make_context):
    result = runner.invoke(
        app,
        ["event", "show", "2"],
        obj=make_context,
    )
    assert result.exit_code == 0
    assert "ID:" in result.output


def test_event_show_invalid(make_context):
    result = runner.invoke(app, ["event", "show", "9999"], obj=make_context)
    assert result.exit_code == 0
    assert "non trouvé" in result.output.lower()


def test_event_list(make_context):
    result = runner.invoke(app, ["event", "list"],obj=make_context)
    assert result.exit_code == 0
    assert "Événements" in result.output or "événement" in result.output.lower()


def test_event_list_invalid_filter(make_context):
    result = runner.invoke(app, ["event", "list", "-f", "invalid"], obj=make_context)
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_event_list_valid_filter(make_context):
    result = runner.invoke(app, ["event", "list", "-f", "no-support"], obj=make_context)
    assert result.exit_code == 0


def test_event_assign():
    create_result = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            "149\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        ),
        obj={
            "current_user": {
                "user_current_id": 132,
                "user_current_role": Role.COMMERCIAL,
            },
        }
    )

    match = re.search(r"Evènement\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout
    event_id = match.group(1)

    result = runner.invoke(
        app, ["event", "assign", event_id],
        input="60\n",
        obj={
            "current_user": {
                "user_current_id": 101,
                "user_current_role": Role.GESTION,
            },
        }
    )
    assert result.exit_code == 0
    assert "assigné" in result.output

def test_contrat_delete_valid():
    create_result = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            "149\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        ),
        obj={
            "current_user": {
                "user_current_id": 132,
                "user_current_role": Role.COMMERCIAL,
            },
        }
    )

    match = re.search(r"Evènement\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout

    event_id = match.group(1)

    delete_result = runner.invoke(
        app, ['event', "delete", event_id],
        obj={
            "current_user": {
                "user_current_id": 132,
                "user_current_role": Role.ADMIN,
            },
        },
        input="y\n",
    )

    assert f"Evènement #{event_id} supprimé" in delete_result.stdout
    assert delete_result.exit_code == 0
