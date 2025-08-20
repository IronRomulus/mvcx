import click
from alembic.command import revision, upgrade
from alembic.config import Config

_alembic_cfg = Config("alembic.ini")


@click.command()
def makemigrations() -> None:
    revision(_alembic_cfg, autogenerate=True)


@click.command()
def migrate() -> None:
    upgrade(_alembic_cfg, "head")
