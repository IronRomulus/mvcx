from pathlib import Path

import click

from mvcx._cli._config import APP_FILES
from mvcx._cli._utils import copy_files


@click.command()
@click.argument("name", type=str)
def startapp(name: str) -> None:
    app_path = Path(f"src/{name}")

    if app_path.exists():
        overwrite: bool = click.prompt(
            "It looks like you have an existing file or directory here. Do you want to overwrite it? [y/N]",
            type=bool,
            default=False,
            show_default=False,
        )

        if not overwrite:
            return

    copy_files(APP_FILES, Path(f"src/{name}"))
