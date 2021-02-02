"""Commands for building a wheel."""
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import yaml
from pydantic import ValidationError

from custom_wheels._constants import BuildTypes, BuildVersions
from custom_wheels._exceptions import CustomWheelError
from custom_wheels._models import Spec, SpecFile

_logger = logging.getLogger(__name__)

WORKING_DIR = Path().resolve()
OUTPUT_DIR = Path(WORKING_DIR, "dist")


def _get_spec_by_version(specfile: SpecFile, spec_version: int) -> Spec:
    try:
        spec = specfile.versions[spec_version]
    except KeyError:
        raise CustomWheelError("Invalid spec version provided")
    return spec


def _get_spec_by_package_version(
    specfile: SpecFile, package_version: str
) -> Tuple[Spec, int]:
    for spec_version, spec in specfile.versions.items():
        package_versions = (
            [] if spec.package_versions is None else spec.package_versions
        )
        if package_version in package_versions:
            return spec, spec_version
    raise CustomWheelError("Package version not included in any Spec")


def _get_package_spec(
    name: str, version: str, spec_version: Optional[int]
) -> Tuple[Spec, int]:
    try:
        spec_file_content = Path(
            WORKING_DIR, "package_specs", f"{name}.yaml"
        ).read_text()
    except FileNotFoundError:
        raise CustomWheelError(f"Could not find the spec for {name}")

    try:
        package_spec_dict = yaml.safe_load(spec_file_content)
        specfile = SpecFile(**package_spec_dict)
    except (yaml.YAMLError, TypeError, ValidationError):
        raise CustomWheelError(f"Specfile for {name} is invalid!")

    # If spec version is provided, use that
    # If not, see if the version of the package to build is included in an existing spec
    # If not, default to using the most recent spec version
    if spec_version is not None:
        spec = _get_spec_by_version(specfile, spec_version)
    else:
        try:
            spec, spec_version = _get_spec_by_package_version(specfile, version)
        except CustomWheelError:
            spec_version = max(specfile.versions.keys())
            spec = specfile.versions[spec_version]
    return spec, spec_version


def _set_environment_variables(variables: Optional[Dict[str, str]]) -> None:
    if variables is not None:
        os.environ.update(variables)


def _run_subprocess(commands: Union[List[str], str], err_message: str, **kwargs: Any):
    ret_code = subprocess.call(commands, **kwargs)  # nosec
    if ret_code != 0:
        raise CustomWheelError(err_message)


def _pip_install(
    dependencies: Optional[List[str]], build_version: BuildVersions
) -> None:
    pip = f"/opt/python/{build_version}/bin/pip"
    pip_install_command = [pip, "install"]
    if dependencies:
        pip_install_command.extend(dependencies)
        _run_subprocess(pip_install_command, "Error installing pip dependencies")


def _yum_install(dependencies: Optional[List[str]]) -> None:
    yum_install_commands = ["yum", "install", "-y"]
    if dependencies:
        _logger.info("Installing system dependencies")
        yum_install_commands.extend(dependencies)
        _run_subprocess(yum_install_commands, "Error installing yum dependencies")


def _execute_bash(commands: Optional[List[str]]) -> None:
    if commands:
        _logger.info("Executing bash_commands")
        for command in commands:
            _run_subprocess(
                command, "Error executing bash commands.", shell=True  # nosec
            )


def _build_wheel(
    package_name: str,
    package_version: str,
    build_version: BuildVersions,
    spec_version: int,
) -> None:
    _logger.info(f"Building {package_name}=={package_version} on {build_version}")
    command = [
        "build_wheel",
        build_version,
        package_name,
        package_version,
        str(spec_version),
    ]
    build_failure_message = (
        f"Error building {package_name}=={package_version} on {build_version}"
    )
    _run_subprocess(command, build_failure_message)


def build_wheels(
    package_name: str,
    package_version: str,
    spec_version: int = None,
    py_versions: Iterable[BuildTypes] = None,
) -> None:
    """
    Build wheels for specified package and output them in /dist/validated.

    :param package_name: Name of package
    :param package_version: Version of package to build
    :param spec_version: (Optional) Specfile version to use. If none provided,
        checks if package version is listed in the specfile. Otherwise, defaults
        to the most recent spec.
    :param py_versions: (Optional) Versions of python to build wheels for.
        If none provided, will build wheels for all supported Python versions.
    """
    package, spec_version = _get_package_spec(
        package_name, package_version, spec_version
    )

    _logger.info(f"Preparing environment to build wheels for {package_name}")
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    _set_environment_variables(package.environment_variables)
    _execute_bash(package.bash_commands)
    _yum_install(package.system_dependencies)

    versions = [BuildVersions[v] for v in py_versions] if py_versions else None

    for build_version in versions or BuildVersions:
        _pip_install(package.python_package_dependencies, build_version)
        _build_wheel(package_name, package_version, build_version, spec_version)
