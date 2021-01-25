import logging
import os
from pathlib import Path
from typing import Dict

from toml import TomlDecodeError
from toml import load as load_toml

from little_cheesemonger._errors import LittleCheesemongerError

LOGGER = logging.getLogger(__name__)


def _determine_platform():
    """Determine platform."""

    platform = None

    # manylinux
    try:
        platform = os.environ["AUDITWHEEL_PLAT"]
    except KeyError:
        LOGGER.debug("Unable to identify platform as 'manylinux'")

    if platform is None:
        raise LittleCheesemongerError("Unable to determine platform")

    return platform


def default_loader(directory: Path) -> Dict[str, str]:
    """Default configuration loader."""

    # load pyproject.toml file
    try:
        pyproject_data = load_toml(directory / "pyproject.toml")
    except (TomlDecodeError, FileNotFoundError) as e:
        raise LittleCheesemongerError(f"Error loading pyproject.toml: {e}")

    # determine platform
    platform = _determine_platform()

    # load package configuration
    try:
        package_data = pyproject_data["tool"]["little-cheesemonger"][platform]
    except KeyError as e:
        raise LittleCheesemongerError(f"Error loading configuration: {e}")

    return package_data
