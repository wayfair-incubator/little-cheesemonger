import os
from pathlib import Path

import pytest
from toml import TomlDecodeError

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._loader import default_loader
from tests.constants import PLATFORM


DIRECTORY = Path(".")
PACKAGE_DATA = {"foo": "bar"}
PYPROJECT_DATA = {"tool": {"little-cheesemonger": {PLATFORM: PACKAGE_DATA}}}


@pytest.fixture
def load_toml(mocker):
    return mocker.patch(
        "little_cheesemonger._loader.load_toml", return_value=PYPROJECT_DATA
    )


@pytest.fixture
def get_platform(mocker):
    return mocker.patch(
        "little_cheesemonger._loader.get_platform", return_value=PLATFORM
    )


@pytest.mark.parametrize("error", [(TomlDecodeError("", "", 0),), (FileNotFoundError,)])
def test_default_loader__error__raise_LittleCheesemongerError(error, load_toml):

    load_toml.side_effect = error

    with pytest.raises(
        LittleCheesemongerError, match=r"Error loading pyproject.toml:.*"
    ):
        default_loader(DIRECTORY)


def test_default_loader__KeyError__raise_LittleCheesemongerError(
    load_toml, get_platform
):

    load_toml.return_value = {}

    with pytest.raises(
        LittleCheesemongerError, match=r"Error loading configuration for platform .*"
    ):
        default_loader(DIRECTORY)


def test_default_loader__return_package_data(load_toml, get_platform):
    assert default_loader(DIRECTORY) == PACKAGE_DATA
