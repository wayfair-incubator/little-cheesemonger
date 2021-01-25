import os
from pathlib import Path

import pytest
from toml import TomlDecodeError

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._loader import _determine_platform, default_loader

PLATFORM = "test_platform"
DIRECTORY = Path(".")
PACKAGE_DATA = {"foo": "bar"}
PYPROJECT_DATA = {"tool": {"little-cheesemonger": {PLATFORM: PACKAGE_DATA}}}


@pytest.fixture
def os_environ(mocker):
    return mocker.patch.dict(os.environ, {"AUDITWHEEL_PLAT": PLATFORM})


@pytest.fixture
def load_toml(mocker):
    return mocker.patch(
        "little_cheesemonger._loader.load_toml", return_value=PYPROJECT_DATA
    )


@pytest.fixture
def determine_platform(mocker):
    return mocker.patch(
        "little_cheesemonger._loader._determine_platform", return_value=PLATFORM
    )


def test_determine_platform__return_platform_name(os_environ):
    assert _determine_platform() == PLATFORM


def test_determine_platform__raise_LittleCheesemongerError():
    with pytest.raises(LittleCheesemongerError):
        _determine_platform()


def test_default_loader__TomlDecodeError__raise_LittleCheesemongerError(load_toml):

    load_toml.side_effect = TomlDecodeError("", "", 0)

    with pytest.raises(LittleCheesemongerError):
        default_loader(DIRECTORY)


def test_default_loader__FileNotFoundError__raise_LittleCheesemongerError(load_toml):

    load_toml.side_effect = FileNotFoundError

    with pytest.raises(LittleCheesemongerError):
        default_loader(DIRECTORY)


def test_default_loader__KeyError__raise_LittleCheesemongerError(
    load_toml, determine_platform
):

    load_toml.return_value = {}

    with pytest.raises(LittleCheesemongerError):
        default_loader(DIRECTORY)


def test_default_loader__return_package_data(load_toml, determine_platform):
    assert default_loader(DIRECTORY) == PACKAGE_DATA
