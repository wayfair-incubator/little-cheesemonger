import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Dict

from little_cheesemonger._constants import (
    PYTHON_BINARIES,
    Architecture,
    Platform,
    PythonVersion,
)
from little_cheesemonger._errors import LittleCheesemongerError

LOGGER = logging.getLogger(__name__)


@lru_cache
def get_platform() -> str:
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


def get_python_binaries() -> Dict[PythonVersion, Path]:
    """Return a dict mapping of PythonVersion to Path object of the
    path to the Python binaries (python, pip etc) for that version.
    """

    platform, architecture = get_platform().split("_", 1)

    print(platform, architecture)

    try:
        return PYTHON_BINARIES[Architecture[architecture]][Platform[platform]]
    except KeyError:
        raise LittleCheesemongerError(
            "No value in PYTHON_BINARIES constant for architecture or platform."
        )
