import logging
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

from little_cheesemonger._constants import (
    PYTHON_BINARIES,
    Architecture,
    Platform,
    PythonVersion,
)
from little_cheesemonger._errors import LittleCheesemongerError

LOGGER = logging.getLogger(__name__)
PLATFORM_PATTERN = ".+_.+"  # NOTE: <platform>_<architecture>


def get_platform_manylinux() -> Optional[str]:
    """Check for platform string in location provided by
    manylinux images.

    :return: The identified platform
    :rtype: str, None
    """

    platform = os.environ.get("AUDITWHEEL_PLAT")

    if platform is None:
        LOGGER.debug("AUDITWHEEL_PLAT environment variable not set")
        return None

    if not re.match(PLATFORM_PATTERN, platform):
        LOGGER.debug(
            f"AUDITWHEEL_PLAT environment variable value {platform} "
            "does not match PLATFORM_ARCHITECTURE pattern"
        )
        return None

    return platform


GET_PLATFORM_FUNCTIONS = (get_platform_manylinux,)


@lru_cache(maxsize=None)
def get_platform() -> str:
    """Determine the platform prior to executing a loader.

    :raises LittleCheesemongerError: Unable to identify the platform.
    """

    for function in GET_PLATFORM_FUNCTIONS:
        platform = function()
        if platform is not None:
            return platform

    raise LittleCheesemongerError("Unable to determine platform")


def get_python_binaries() -> Dict[PythonVersion, Path]:
    """Return a dict mapping of PythonVersion to Path object of the
    path to the Python binaries (python, pip etc) for that version.
    """

    platform, architecture = get_platform().split("_", 1)

    try:
        return PYTHON_BINARIES[Architecture[architecture]][Platform[platform]]
    except KeyError:
        raise LittleCheesemongerError(
            "No value in PYTHON_BINARIES constant for "
            f"architecture `{architecture}` or "
            f"platform `{platform}`"
        )
