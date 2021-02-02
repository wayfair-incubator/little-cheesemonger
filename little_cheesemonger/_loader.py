import logging
import os
from pathlib import Path
from typing import Dict

from toml import TomlDecodeError
from toml import load as load_toml

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._platform import get_platform


LOGGER = logging.getLogger(__name__)


def default_loader(directory: Path) -> Dict[str, str]:
    """Default configuration loader. Loads package configuration from
    pyproject.toml file in `directory` and returns data from configuration
    section for platform identified by `_determine_platform` call.

    :param directory: Path instance representing path to directory
        containing pyproject.toml file.
    :raises LittleCheesemongerError: Unable to locate or decode `pyproject.toml`
    file, or unable to locate package data within file.
    """

    # load pyproject.toml file
    try:
        pyproject_data = load_toml(directory / "pyproject.toml")
    except (TomlDecodeError, FileNotFoundError) as e:
        raise LittleCheesemongerError(f"Error loading pyproject.toml: {e}")

    platform = get_platform()

    # load package configuration
    try:
        package_data = pyproject_data["tool"]["little-cheesemonger"][platform]
    except KeyError as e:
        raise LittleCheesemongerError(
            f"Error loading configuration for platform {platform}: {e}"
        )

    return package_data
