import click

from .base import cmdjob
from .dumpdummy import dumpdummy

cli = click.CommandCollection(sources=[cmdjob])


__all__ = ["dumpdummy"]
