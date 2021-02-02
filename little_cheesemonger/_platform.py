import os
import logging

from functools import lru_cache

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._constants import PythonVersion, PYTHON_BINARIES


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


def get_python_binaries(python_version: PythonVersion) -> None:
    """ Return Path to Python binaries (python, pip) given a 
    detectable platform and PythonVersion.
    """
    
    platform, architecture = get_platform.split("=", 1)
    
    return PYTHON_BINARIES[architecture][platform][python_version]
