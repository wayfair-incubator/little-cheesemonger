import logging
from pathlib import Path
from typing import Optional

import click

from little_cheesemonger._errors import LittleCheesemongerError

LOGGER = logging.getLogger(__name__)


@click.command()
@click.argument("directory", type=Path, default=Path("."))
@click.option("--debug", is_flag=True)
@click.option("-dl", "--data-loader")
@click.option("-dla", "--data-loader-arg", "data_loader_args", multiple=True)
def entrypoint(
    directory: Path,
    debug: bool = False,
    data_loader: Optional[str] = None,
    data_loader_args: Optional[list] = None,
):

    """
    Parse and handle CLI arguments.

    :param directory: The directory from which to load configuration data. Typically a python package
        containing a `pyproject.toml` file. Defaults to the local directory.
    :param debug: If set to True, sets log level for the application to DEBUG.
    :param data_loader: Optional. Path to a class implementing a custom data loader in
        Python import synxtax ex. "package.module.class".
    :param data_loader_args: Additional positional arguments to be passed to a custom data loader.
        NOTE: Arguments are passed after the `directory` argument in the order they are set.
    :raises LittleCheesemongerError: Data loader arguments are set without a custom data loader.
    """

    logging.getLogger("little_cheesemonger").setLevel("DEBUG" if debug else "WARNING")

    try:
        if data_loader_args and data_loader is None:
            raise LittleCheesemongerError(
                "Additional data loader arguments can only be used with a custom data loader."
            )

    except LittleCheesemongerError as e:
        LOGGER.error(e)
        exit(1)
