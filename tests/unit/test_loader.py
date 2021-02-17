import copy

import pytest
from toml import TomlDecodeError

from little_cheesemonger._constants import DEFAULT_CONFIGURATION
from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._loader import (
    default_loader,
    import_loader_function,
    load_configuration,
)
from tests.constants import (
    CONFIGURATION,
    DIRECTORY,
    LOADER_ARGS,
    LOADER_IMPORT_PATH,
    LOADER_KWARGS,
    PLATFORM,
)

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


@pytest.fixture
def getattr_mock(mocker):
    return mocker.patch("little_cheesemonger._loader.getattr")


@pytest.fixture
def import_module(mocker):
    return mocker.patch("little_cheesemonger._loader.import_module", mocker.MagicMock())


@pytest.fixture
def import_loader_function_mock(mocker):
    return mocker.patch(
        "little_cheesemonger._loader.import_loader_function",
        return_value=mocker.Mock(return_value=CONFIGURATION),
    )


@pytest.fixture
def default_loader_mock(mocker):
    return mocker.patch(
        "little_cheesemonger._loader.default_loader", return_value=CONFIGURATION
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
        import_loader_function(LOADER_IMPORT_PATH)


def test_import_loader_function__get_attributte_error__raise_LittleCheesemongerError(
    import_module, getattr_mock
):

    getattr_mock.side_effect = AttributeError

    with pytest.raises(LittleCheesemongerError, match=r"Error importing function .*"):
        import_loader_function(LOADER_IMPORT_PATH)


def test_import_loader_function__function_imported_and_returned(
    import_module, getattr_mock
):

    function = import_loader_function(LOADER_IMPORT_PATH)

    import_module.assert_called()
    assert function == getattr_mock.return_value


def test_load_configuration__loader_import_path_set__import_loader_function_called(
    import_loader_function_mock,
):

    load_configuration(DIRECTORY, LOADER_IMPORT_PATH, LOADER_ARGS, LOADER_KWARGS)

    import_loader_function_mock.assert_called_once()


def test_load_configuration__custom_loader_raises_Exception__raise_LittleCheesemongerError(
    mocker, import_loader_function_mock
):
    import_loader_function_mock.return_value = mocker.Mock(side_effect=Exception)

    with pytest.raises(LittleCheesemongerError, match=r"Error executing loader .*"):
        load_configuration(DIRECTORY, LOADER_IMPORT_PATH, LOADER_ARGS, LOADER_KWARGS)


def test_load_configuration__loader_import_path_not_set__default_loader_called(
    default_loader_mock,
):

    load_configuration(DIRECTORY, None, (), {})

    default_loader_mock.assert_called_once()


def test_load_configuration__loaded_configuration_merged_with_default_configuration(
    default_loader_mock,
):

    configuration_to_load = copy.copy(CONFIGURATION)
    del configuration_to_load["steps"]
    default_loader_mock.return_value = configuration_to_load

    configuration = load_configuration(DIRECTORY, None, (), {})

    assert configuration["steps"] is None
