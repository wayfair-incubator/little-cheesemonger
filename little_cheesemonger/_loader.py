import copy
import logging
from pathlib import Path

from toml import TomlDecodeError
from toml import load as load_toml

from little_cheesemonger._constants import DEFAULT_CONFIGURATION
from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._platform import get_platform
from little_cheesemonger._types import ConfigurationType

LOGGER = logging.getLogger(__name__)


def default_loader(directory: Path) -> ConfigurationType:
    """Default configuration loader. Loads package configuration from
    pyproject.toml file in `directory` and returns data from configuration
    section for platform identified by `get_platform` call.

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

    # normalize configuration with defaults
    configuration = copy.copy(DEFAULT_CONFIGURATION)
    configuration.update(package_data)

    return configuration
