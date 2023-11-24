"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """R2DT API Client."""


if __name__ == "__main__":
    main(prog_name="r2dt-client")  # pragma: no cover
