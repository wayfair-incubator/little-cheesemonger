import os
from pathlib import Path
from unittest.mock import patch

import pytest

from little_cheesemonger._constants import PythonVersion
from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._platform import get_platform, get_python_binaries
from tests.constants import PLATFORM_RAW


@pytest.fixture(autouse=True)
def platform_cache_clear():
    get_platform.cache_clear()
    yield


@pytest.fixture
def os_environ(mocker):
    return mocker.patch.dict(os.environ, {"AUDITWHEEL_PLAT": PLATFORM_RAW})


def test_get_platform__return_platform_name(os_environ):
    assert get_platform() == PLATFORM_RAW


def test_get_platform__environment_variable_not_set__raise_LittleCheesemongerError():
    with pytest.raises(LittleCheesemongerError, match=r"Unable to determine platform"):
        get_platform()


def test_get_platform__unable_to_determine_platform__raise_LittleCheesemongerError(
    mocker,
):

    mocker.patch.dict(os.environ, {"AUDITWHEEL_PLAT": "invalid-format"})

    with pytest.raises(LittleCheesemongerError, match=r"Unable to determine platform"):
        get_platform()


@patch("little_cheesemonger._platform.PYTHON_BINARIES", {})
def test_get_python_binaries__raise_LittleCheesemongerError(mocker):
    mocker.patch(
        "little_cheesemonger._platform.get_platform",
        return_value="manylinux2014_x86_64",
    )

    with pytest.raises(
        LittleCheesemongerError, match=r"No value in PYTHON_BINARIES .*"
    ):
        get_python_binaries()


def test_get_python_binaries__return_binaries_for_architecture_and_platform(mocker):
    mocker.patch(
        "little_cheesemonger._platform.get_platform",
        return_value="manylinux2014_x86_64",
    )
    assert get_python_binaries() == {
        PythonVersion.CP35_CP35M: Path("/opt/python/cp35-cp35m/bin"),
        PythonVersion.CP36_CP36M: Path("/opt/python/cp36-cp36m/bin"),
        PythonVersion.CP37_CP37M: Path("/opt/python/cp37-cp37m/bin"),
        PythonVersion.CP38_CP38: Path("/opt/python/cp38-cp38/bin"),
        PythonVersion.CP39_CP39: Path("/opt/python/cp39-cp39/bin"),
    }
