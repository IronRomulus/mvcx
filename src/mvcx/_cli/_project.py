import subprocess
from pathlib import Path

import click

from mvcx._cli._config import PROJECT_FILES
from mvcx._cli._utils import copy_files


@click.command()
@click.argument("name", type=str, default=".")
def startproject(name: str) -> None:
    project_path = Path(name)

    if project_path.exists() and any(project_path.iterdir()):
        overwrite: bool = click.prompt(
            "It looks like you have existing files or directories here. Do you want to overwrite them? [y/N]",
            type=bool,
            default=False,
            show_default=False,
        )

        if not overwrite:
            return

    if not Path("pyproject.toml").exists():
        subprocess.run(["uv", "init", name])
        Path("main.py").unlink(missing_ok=True)

    copy_files(PROJECT_FILES, project_path)
