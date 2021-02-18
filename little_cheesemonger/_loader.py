import copy
import logging
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

from toml import TomlDecodeError
from toml import load as load_toml

from little_cheesemonger._constants import DEFAULT_CONFIGURATION
from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._platform import get_platform
from little_cheesemonger._types import ConfigurationType

LOGGER = logging.getLogger(__name__)


def default_loader(directory: Path) -> ConfigurationType:
    """Default configuration loader. Loads package configuration from
    pyproject.toml file in `directory` and returns data from configuration
    section for platform identified by `get_platform` call.

    :param directory: Path instance representing path to directory
        containing pyproject.toml file.
    :raises LittleCheesemongerError: Unable to locate or decode `pyproject.toml`
    file, or unable to locate package data within file.
    """

    # load pyproject.toml file
    try:
        pyproject_data = load_toml(directory / "pyproject.toml")
    except (TomlDecodeError, FileNotFoundError) as e:
        raise LittleCheesemongerError(f"Error loading pyproject.toml: {e}")

    platform = get_platform()

    # load package configuration
    try:
        package_data = pyproject_data["tool"]["little-cheesemonger"][platform]
    except KeyError as e:
        raise LittleCheesemongerError(
            f"Error loading configuration for platform {platform}: {e}"
        )

    # normalize configuration with defaults
    configuration = copy.copy(DEFAULT_CONFIGURATION)
    configuration.update(package_data)

    return configuration


def import_loader_function(import_path: str) -> Callable:

    try:
        *module_path, function_name = import_path.split(".")
        if not module_path:
            raise ValueError("Module path cannot be empty")
    except ValueError as e:
        raise LittleCheesemongerError(
            f"Unable to parse loader path `{import_path}`: {e}"
        )

    try:
        module = import_module(".".join(module_path))
    except ModuleNotFoundError as e:
        raise LittleCheesemongerError(f"Error importing module `{module_path}`: {e}")

    try:
        function = getattr(module, function_name)
    except AttributeError as e:
        raise LittleCheesemongerError(
            f"Error importing function `{function_name}` from module `{module_path}`: {e}`"
        )

    return function


def load_configuration(
    directory: Path,
    loader_import_path: Optional[str],
    loader_args: Tuple[Any, ...],
    loader_kwargs: Dict[str, Any],
) -> ConfigurationType:

    configuration: ConfigurationType = copy.copy(DEFAULT_CONFIGURATION)

    if loader_import_path is not None:
        loader = import_loader_function(loader_import_path)

        try:
            loaded_configuration = loader(directory, *loader_args, **loader_kwargs)
        except Exception as e:
            raise LittleCheesemongerError(f"Error executing loader `{loader}`: {e}")

    else:
        loaded_configuration = default_loader(directory)

    configuration.update(loaded_configuration)

    return configuration
