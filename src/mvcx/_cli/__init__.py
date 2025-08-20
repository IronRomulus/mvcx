from importlib import metadata

import click

from mvcx._cli._app import startapp
from mvcx._cli._migrations import makemigrations, migrate
from mvcx._cli._project import startproject
from mvcx._cli._server import dev, start


@click.group(invoke_without_command=True)
@click.option("--version", "-v", type=bool, is_flag=True)
def cli(version: bool):
    if version:
        click.secho(f"Version {metadata.version('mvcx')}")


cli.add_command(startproject)
cli.add_command(startapp)

cli.add_command(start)
cli.add_command(dev)

cli.add_command(makemigrations)
cli.add_command(migrate)
