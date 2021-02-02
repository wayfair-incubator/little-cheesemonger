from enum import Enum
from pathlib import Path

PLATFORM = "platform"
ARCHITECTURE = "architecture"
PYTHON_VERSION = "foo38"
PYTHON_BINARIES_PATH = Path("foo/bar")
PLATFORM_RAW = f"{PLATFORM}_{ARCHITECTURE}"


class Architecture(str, Enum):
    architecture = ARCHITECTURE


class Platform(str, Enum):
    platform = PLATFORM


PYTHON_BINARIES = {
    Architecture.architecture: {
        Platform.platform: {PYTHON_VERSION: PYTHON_BINARIES_PATH}
    }
}
