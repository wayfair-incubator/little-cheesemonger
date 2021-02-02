import logging
from pathlib import Path
from typing import Dict, Optional, Tuple

import click

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._loader import default_loader
from little_cheesemonger._run import run

LOGGER = logging.getLogger(__name__)


@click.command()
@click.argument("directory", type=Path, default=Path("."))
@click.option("-l", "--loader")
@click.option("-la", "--loader-arg", "loader_args", multiple=True)
@click.option("-lk", "--loader-kwarg", "loader_kwargs_raw", multiple=True)
@click.option("--debug", is_flag=True)
def entrypoint(
    directory: Path,
    loader: Optional[str],
    loader_args: Tuple[str, ...],
    loader_kwargs_raw: Tuple[str, ...],
    debug: bool,
):

    """
    Parse and handle CLI arguments.

    :param directory: The directory from which to load configuration data. Typically a python package
        containing a `pyproject.toml` file. Defaults to the local directory.
    :param debug: If set to True, sets log level for the application to DEBUG.
    :param loader: Optional. Path to a class implementing a custom loader in
        Python import synxtax ex. "package.module.class".
    :param loader_args: Additional positional arguments to be passed to a custom loader.
        NOTE: Arguments are passed after the `directory` argument in the order they are set.
    :raises LittleCheesemongerError: Loader arguments are set without a custom loader.
    """

    logging.getLogger("little_cheesemonger").setLevel("DEBUG" if debug else "WARNING")

    try:

        if (loader_args or loader_kwargs_raw) and loader is None:
            raise LittleCheesemongerError(
                "Additional loader arguments can only be used with a custom loader."
            )

        if loader is not None:
            if loader_kwargs_raw:
                _process_kwargs(loader_kwargs_raw)

        else:
            configuration = default_loader(directory)
            
        run(configuration)

    except LittleCheesemongerError as e:
        LOGGER.error(e)
        exit(1)


def _process_kwargs(raw_kwargs: Tuple[str, ...]) -> Dict[str, str]:
    kwargs: Dict[str, str] = {}

    for raw_kwarg in raw_kwargs:
        try:
            key, value = raw_kwarg.split("=")
        except ValueError:
            raise LittleCheesemongerError(
                f"Invalid keyword argument '{raw_kwarg}' received for --loader-kwarg option. "
                "Keyword arguments must be in KEY=VALUE format."
            )
        kwargs[key] = value

    return kwargs
