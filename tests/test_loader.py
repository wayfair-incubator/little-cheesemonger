import copy
from pathlib import Path

import pytest
from toml import TomlDecodeError

from little_cheesemonger._constants import DEFAULT_CONFIGURATION
from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._loader import default_loader, import_loader_function
from tests.constants import PLATFORM

DIRECTORY = Path(".")
PACKAGE_DATA = {"foo": "bar"}
PYPROJECT_DATA = {"tool": {"little-cheesemonger": {PLATFORM: PACKAGE_DATA}}}
LOADER_FUNCTION_IMPORT_PATH = "foo.bar"


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


@pytest.fixture
def getattr_mock(mocker):
    return mocker.patch("little_cheesemonger._loader.getattr")


@pytest.fixture
def import_module(mocker):
    return mocker.patch("little_cheesemonger._loader.import_module", mocker.MagicMock())


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

    expected_configuration = copy.copy(DEFAULT_CONFIGURATION)
    expected_configuration.update(PACKAGE_DATA)

    assert default_loader(DIRECTORY) == expected_configuration


def test_import_loader_function__import_path_invalid_format__raise_LittleCheesemongerError():

    with pytest.raises(LittleCheesemongerError, match=r"Unable to parse .*"):
        import_loader_function("invalid")


def test_import_loader_function__import_module_error__raise_LittleCheesemongerError(
    import_module,
):

    import_module.side_effect = ModuleNotFoundError

    with pytest.raises(LittleCheesemongerError, match=r"Error importing module .*"):
        import_loader_function(LOADER_FUNCTION_IMPORT_PATH)


def test_import_loader_function__get_attributte_error__raise_LittleCheesemongerError(
    import_module, getattr_mock
):

    getattr_mock.side_effect = AttributeError

    with pytest.raises(LittleCheesemongerError, match=r"Error importing function .*"):
        import_loader_function(LOADER_FUNCTION_IMPORT_PATH)


def test_import_loader_function__function_imported_and_returned(
    import_module, getattr_mock
):

    function = import_loader_function(LOADER_FUNCTION_IMPORT_PATH)

    import_module.assert_called()
    assert function == getattr_mock.return_value
