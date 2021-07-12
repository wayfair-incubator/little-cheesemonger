from enum import Enum
from pathlib import Path

from little_cheesemonger._types import ConfigurationType


class Architecture(str, Enum):
    X86_64 = "x86_64"


class Platform(str, Enum):
    MANYLINUX1 = "manylinux1"
    MANYLINUX2010 = "manylinux2010"
    MANYLINUX2014 = "manylinux2014"


class PythonVersion(str, Enum):
    CP27_CP27M = "cp27-cp27m"
    CP27_CP27MU = "cp27-cp27mu"
    CP35_CP35M = "cp35-cp35m"
    CP36_CP36M = "cp36-cp36m"
    CP37_CP37M = "cp37-cp37m"
    CP38_CP38 = "cp38-cp38"
    CP39_CP39 = "cp39-cp39"


PYTHON_BINARIES = {
    Architecture.X86_64: {
        Platform.MANYLINUX1: {
            PythonVersion.CP27_CP27M: Path("/opt/python/cp27-cp27m/bin"),
            PythonVersion.CP27_CP27MU: Path("/opt/python/cp27-cp27mu/bin"),
            PythonVersion.CP35_CP35M: Path("/opt/python/cp35-cp35m/bin"),
            PythonVersion.CP36_CP36M: Path("/opt/python/cp36-cp36m/bin"),
            PythonVersion.CP37_CP37M: Path("/opt/python/cp37-cp37m/bin"),
            PythonVersion.CP38_CP38: Path("/opt/python/cp38-cp38/bin"),
            PythonVersion.CP39_CP39: Path("/opt/python/cp39-cp39/bin"),
        },
        Platform.MANYLINUX2010: {
            PythonVersion.CP35_CP35M: Path("/opt/python/cp35-cp35m/bin"),
            PythonVersion.CP36_CP36M: Path("/opt/python/cp36-cp36m/bin"),
            PythonVersion.CP37_CP37M: Path("/opt/python/cp37-cp37m/bin"),
            PythonVersion.CP38_CP38: Path("/opt/python/cp38-cp38/bin"),
            PythonVersion.CP39_CP39: Path("/opt/python/cp39-cp39/bin"),
        },
        Platform.MANYLINUX2014: {
            PythonVersion.CP35_CP35M: Path("/opt/python/cp35-cp35m/bin"),
            PythonVersion.CP36_CP36M: Path("/opt/python/cp36-cp36m/bin"),
            PythonVersion.CP37_CP37M: Path("/opt/python/cp37-cp37m/bin"),
            PythonVersion.CP38_CP38: Path("/opt/python/cp38-cp38/bin"),
            PythonVersion.CP39_CP39: Path("/opt/python/cp39-cp39/bin"),
        },
    }
}

DEFAULT_CONFIGURATION: ConfigurationType = {
    "environment_variables": None,
    "system_dependencies": None,
    "python_dependencies": None,
    "python_versions": None,
    "steps": None,
}
