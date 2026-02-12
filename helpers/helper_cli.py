from rich.console import Console
from rich.panel import Panel

console = Console()

def error_display(title, message):
    """ Display error message """
    content = f" {message} "
    panel = Panel(
        content,
        title=f"[bold bright_red]{title}[/bold bright_red]",
        border_style="red",
        expand=False,
        padding=1,
    )
    console.print(panel)
