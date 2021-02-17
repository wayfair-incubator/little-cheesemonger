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

DIRECTORY = Path(".")
LOADER_IMPORT_PATH = "foo.bar"
LOADER_ARGS = ("foo",)
LOADER_KWARGS = {"foo": "bar"}
ENVIRONMENT_VARIABLES = ["foo=bar"]
SYSTEM_DEPENDENCIES = ["foo-1.0.0"]
PYTHON_DEPENDENCIES = ["foo==1.0.0"]
STEPS = ["foo"]
CONFIGURATION = {
    "environment_variables": ENVIRONMENT_VARIABLES,
    "system_dependencies": SYSTEM_DEPENDENCIES,
    "python_dependencies": PYTHON_DEPENDENCIES,
    "steps": STEPS,
}
