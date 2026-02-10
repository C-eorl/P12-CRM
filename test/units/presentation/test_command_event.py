import re
from typer.testing import CliRunner

from src.presentation.cli.cli_main import app

runner = CliRunner()


def test_event_create():
    result = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            "2\n"
            "2\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        ),
    )

    assert "créé" in result.output
    assert result.exit_code == 0


def test_event_update():
    result = runner.invoke(
        app, ["event", "update", "1"],
        input=(
            "Conférence modifiée\n"
            "2027-01-02 09:00:00\n"
            "2027-01-02 17:00:00\n"
            "Lyon\n"
            "150\n"
            "Nouvelles notes\n"
        ),
    )

    assert result.exit_code == 0
    assert "modifié" in result.output


def test_event_update_invalid_id():
    result = runner.invoke(
        app, ["event", "update", "9999"]
    )

    assert result.exit_code == 0
    assert "Client non trouvé" in result.output


def test_event_show():
    result = runner.invoke(app, ["event", "show", "1"])
    assert result.exit_code == 0
    assert "ID:" in result.output


def test_event_show_invalid():
    result = runner.invoke(app, ["event", "show", "9999"])
    assert result.exit_code == 0
    assert "non trouvé" in result.output.lower()


def test_event_list():
    result = runner.invoke(app, ["event", "list"])
    assert result.exit_code == 0
    assert "Événements" in result.output or "événement" in result.output.lower()


def test_event_list_invalid_filter():
    result = runner.invoke(app, ["event", "list", "-f", "invalid"])
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_event_list_valid_filter():
    result = runner.invoke(app, ["event", "list", "-f", "no-support"])
    assert result.exit_code == 0


def test_event_assign():
    create_result = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            "2\n"
            "2\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        ),
    )

    match = re.search(r"Evènement\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout
    event_id = match.group(1)

    result = runner.invoke(
        app, ["event", "assign", event_id],
        input="60\n",
    )
    assert result.exit_code == 0
    assert "assigné" in result.output

def test_contrat_delete_valid():
    create_result = runner.invoke(
        app, ["event", "create"],
        input=(
            "Conférence Python\n"
            "2\n"
            "2\n"
            "2027-01-01 10:00:00\n"
            "2027-01-01 18:00:00\n"
            "Paris\n"
            "120\n"
            "Notes test\n"
        ),
    )

    match = re.search(r"Evènement\s+#(\d+)\s+créé", create_result.stdout)
    assert match, create_result.stdout

    event_id = match.group(1)

    delete_result = runner.invoke(app, ['event', "delete", event_id])

    assert delete_result.exit_code == 0
    assert f"Evènement #{event_id} supprimé" in delete_result.stdout