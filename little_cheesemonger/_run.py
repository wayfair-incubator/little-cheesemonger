import logging
import os
import subprocess  # nosec
from typing import List

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._platform import get_python_binaries

LOGGER = logging.getLogger(__name__)


def run(configuration: dict) -> None:
    """Run build environment setup per configuration."""

    if "environment_variables" in configuration:
        set_environment_variables(configuration["environment_variables"])

    if "system_dependencies" in configuration:
        install_system_dependencies(configuration["system_dependencies"])

    if "python_dependencies" in configuration:
        install_python_dependencies(configuration["python_dependencies"])

    if "steps" in configuration:
        execute_steps(configuration["steps"])


def set_environment_variables(variables: List[str]) -> None:
    """Set environment variables."""

    variables_expanded = {}

    for variable in variables:
        try:
            key, value = variable.split("=")
            variables_expanded[key] = value
        except ValueError:
            raise LittleCheesemongerError(
                "Unable to extract key and value from envrionment "
                f"variable {variable}. Environment variables must be "
                "set in KEY=VALUE format."
            )

    os.environ.update(variables_expanded)


def install_system_dependencies(dependencies: List[str]) -> None:
    """Install system dependencies."""

    run_subprocess(["yum", "install", "-y"] + dependencies)


def install_python_dependencies(dependencies: List[str]) -> None:
    """Install Python dependencies."""

    for _, binaries in get_python_binaries().items():
        run_subprocess([str(binaries / "pip"), "install"] + dependencies)


def execute_steps(commands: List[str]) -> None:
    """Execute multiple commands."""

    for command in commands:
        run_subprocess(command.split(" "))


def run_subprocess(command: List[str]) -> None:
    """Run subprocess."""

    try:
        subprocess.run(command, check=True, shell=True)  # nosec
    except subprocess.CalledProcessError as e:
        raise LittleCheesemongerError(f"Subprocess error: {e.stderr}")
