from enum import Enum
from pathlib import Path

from little_cheesemonger._types import ConfigurationType


class Architecture(str, Enum):
    x86_64 = "x86_64"


class Platform(str, Enum):
    manylinux1 = "manylinux1"
    manylinux2010 = "manylinux2010"
    manylinux2014 = "manylinux2014"


class PythonVersion(str, Enum):
    cp27_cp27m = "cp27-cp27m"
    cp27_cp27mu = "cp27-cp27mu"
    cp35_cp35m = "cp35-cp35m"
    cp36_cp36m = "cp36-cp36m"
    cp37_cp37m = "cp37-cp37m"
    cp38_cp38 = "cp38-cp38"
    cp39_cp39 = "cp39-cp39"


PYTHON_BINARIES = {
    Architecture.x86_64: {
        Platform.manylinux1: {
            PythonVersion.cp27_cp27m: Path("/opt/python/cp27-cp27m/bin"),
            PythonVersion.cp27_cp27mu: Path("/opt/python/cp27-cp27mu/bin"),
            PythonVersion.cp35_cp35m: Path("/opt/python/cp35-cp35m/bin"),
            PythonVersion.cp36_cp36m: Path("/opt/python/cp36-cp36m/bin"),
            PythonVersion.cp37_cp37m: Path("/opt/python/cp37-cp37m/bin"),
            PythonVersion.cp38_cp38: Path("/opt/python/cp38-cp38/bin"),
            PythonVersion.cp39_cp39: Path("/opt/python/cp39-cp39/bin"),
        },
        Platform.manylinux2010: {
            PythonVersion.cp35_cp35m: Path("/opt/python/cp35-cp35m/bin"),
            PythonVersion.cp36_cp36m: Path("/opt/python/cp36-cp36m/bin"),
            PythonVersion.cp37_cp37m: Path("/opt/python/cp37-cp37m/bin"),
            PythonVersion.cp38_cp38: Path("/opt/python/cp38-cp38/bin"),
            PythonVersion.cp39_cp39: Path("/opt/python/cp39-cp39/bin"),
        },
        Platform.manylinux2014: {
            PythonVersion.cp35_cp35m: Path("/opt/python/cp35-cp35m/bin"),
            PythonVersion.cp36_cp36m: Path("/opt/python/cp36-cp36m/bin"),
            PythonVersion.cp37_cp37m: Path("/opt/python/cp37-cp37m/bin"),
            PythonVersion.cp38_cp38: Path("/opt/python/cp38-cp38/bin"),
            PythonVersion.cp39_cp39: Path("/opt/python/cp39-cp39/bin"),
        },
    }
}

DEFAULT_CONFIGURATION: ConfigurationType = {
    "environment_variables": None,
    "system_dependencies": None,
    "python_dependencies": None,
    "steps": None,
}
