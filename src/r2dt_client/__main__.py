"""Command-line interface."""
from pathlib import Path

import typer
from rich import print


app = typer.Typer()


@app.command()
def draw(filename: Path) -> None:
    """Draw an mRNA sequence as an SVG image."""
    print(f"drawing data from {filename}")


@app.command()
def run(filename: str) -> None:
    """Run an mRNA sequence as an SVG image."""
    print(f"running data from {filename}")


main = app
