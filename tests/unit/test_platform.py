import os

import pytest

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._platform import get_platform, get_python_binaries
from tests.constants import PLATFORM_RAW, PYTHON_BINARIES, Architecture, Platform


@pytest.fixture(autouse=True)
def platform_cache_clear():
    get_platform.cache_clear()
    yield


@pytest.fixture
def os_environ(mocker):
    return mocker.patch.dict(os.environ, {"AUDITWHEEL_PLAT": PLATFORM_RAW})


@pytest.fixture
def architecture_mock(mocker):
    return mocker.patch("little_cheesemonger._platform.Architecture", Architecture)


@pytest.fixture
def platform_mock(mocker):
    return mocker.patch("little_cheesemonger._platform.Platform", Platform)


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


def test_get_python_binaries__return_binaries_for_architecture_and_platform(
    os_environ, mocker, architecture_mock, platform_mock
):

    mocker.patch.dict("little_cheesemonger._platform.PYTHON_BINARIES", PYTHON_BINARIES)

    assert (
        get_python_binaries()
        == PYTHON_BINARIES[Architecture.ARCHITECTURE][Platform.PLATFORM]
    )


def test_get_python_binaries__raise_LittleCheesemongerError(os_environ, mocker):

    mocker.patch.dict("little_cheesemonger._platform.PYTHON_BINARIES", {})

    with pytest.raises(
        LittleCheesemongerError, match=r"No value in PYTHON_BINARIES .*"
    ):
        get_python_binaries()
