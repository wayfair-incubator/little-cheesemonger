import logging
import os
from pathlib import Path
from typing import Dict

from toml import TomlDecodeError
from toml import load as load_toml

from little_cheesemonger._errors import LittleCheesemongerError

LOGGER = logging.getLogger(__name__)


def _determine_platform() -> str:
    """Determine the platform prior to executing a loader. Detection of
    additional platforms beyond `manylinux` should happen here.

    :raises LittleCheesemongerError: Unable to identify the platform.
    """

    platform = None

    try:
        # NOTE: AUDITWHEEL_PLAT envvar set here
        # https://github.com/pypa/manylinux/blob/master/docker/Dockerfile-x86_64#L6
        platform = os.environ["AUDITWHEEL_PLAT"]
    except KeyError:
        LOGGER.debug("Unable to identify platform as 'manylinux'")

    if platform is None:
        raise LittleCheesemongerError("Unable to determine platform")

    return platform


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

    # determine platform
    platform = _determine_platform()

    # load package configuration
    try:
        package_data = pyproject_data["tool"]["little-cheesemonger"][platform]
    except KeyError as e:
        raise LittleCheesemongerError(
            f"Error loading configuration for platform {platform}: {e}"
        )

    return package_data
