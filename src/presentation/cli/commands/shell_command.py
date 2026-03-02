import typer
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from helpers.helper_cli import error_display
from src.infrastructures.security.security import TokenStore

shell_app =typer.Typer()
console = Console()

@shell_app.command(name="start")
def shell():
    from src.presentation.cli.cli_main import app
    TokenStore.delete_token()
    header()
    while True:
        try:
            console.rule(style="white")
            cmd = input("\n>>> ")

            if cmd.strip() in ["exit", "quit"]:
                break

            parts = cmd.strip().split()
            if not parts:
                continue
            try:
                app(args=parts)
            except SystemExit: pass

        except Exception as e:
            error_display("Erreur", e)



def header():
    letters = {
        "E": [
            "█████",
            "█░░░░",
            "████░",
            "█░░░░",
            "█████"
        ],
        "P": [
            "█████",
            "█░░░█",
            "█████",
            "█░░░░",
            "█░░░░"
        ],
        "I": [
            "█████",
            "░░█░░",
            "░░█░░",
            "░░█░░",
            "█████"
        ],
        "C": [
            "█████",
            "█░░░░",
            "█░░░░",
            "█░░░░",
            "█████"
        ],
        "V": [
            "█░░░█",
            "█░░░█",
            "░█░█░",
            "░█░█░",
            "░░█░░"
        ],
        "N": [
            "█░░░█",
            "██░░█",
            "█░█░█",
            "█░░██",
            "█░░░█"
        ],
        "T": [
            "█████",
            "░░█░░",
            "░░█░░",
            "░░█░░",
            "░░█░░"
        ],
        "S": [
            "░████",
            "█░░░░",
            "░███░",
            "░░░░█",
            "████░"
        ],
        # ... compléter pour chaque lettre
    }

    def print_word(word):
        lines = [""] * 5  # 5 lignes par lettre
        for c in word:
            char_lines = letters.get(c.upper(), ["     "] * 5)
            for i in range(5):
                lines[i] += char_lines[i] + "  "
        return "\n".join(lines)

    def content():
        contenu = Text()
        contenu.append(print_word("EPIC EVENTS"))

        return contenu

    panel = Panel(
        Align.center(content()),
        border_style="white",
        box=box.ROUNDED,

        padding=2,
    )
    console.print(panel)
    console.print("v 0.1 by florian rocher", justify="left", style="italic")
    console.print("CRM - Epic Events permettant la gestion Client, Contrat, Évènement et Utilisateur", style="bold")
    console.print("Bienvenue dans le shell interactif ! Tape 'exit' ou 'quit' pour quitter.")
    console.print("\n Veuillez vous connecter, tapez 'auth login'", style="bold")