import logging

from typing import List

from little_cheesemonger._loader import get_platform
from little_cheesemonger._constants import PythonVersion
from little_cheesemonger._platform import get_python_binaries


LOGGER = logging.getLogger(__name__)


def run(configuration: dict) -> None:
    """ Run build environment setup per configuration.
    """
    
    platform = get_platform()
    
    if "environment_variables" in configuration:
        set_environment_variables(configuration["environment_variables"])
        
    if "system_dependencies" in configuration:
        install_system_dependencies(configuraton["system_dependencies"])
        
    if "python_dependencies" in configuration:
        install_python_dependencies(configuration["python_dependencies"])
        
    if "steps" in configuration:
        execute_commands(configuration["steps"])


def set_environment_variables(variables: List[str]) -> None:
    """ Set environment variables.
    """
    
    variables_expanded = {}
    
    for variables in variables:
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
    """ Install system dependencies.
    """

    command = ["yum", "install", "-y"] + dependencies
    run_subprocess(command)


def install_python_dependencies(dependencies: List[str]) -> None:
    """ Install Python dependencies.
    """
    
    for python_version in PythonVersion:
        command = [get_python_binaries(python_version) + "pip", "install"] + dependencies
        run_subprocess(command)


def execute_commands(commands: List[str]) -> None:
    """ Execute multiple commands.
    """
    
    for command in commands:
        run_subprocess(command)


def run_subprocess(command: str) -> None:
    """ Run subprocess.
    """
    
    return_code = subprocess.call(command, shell=True)
    if return_code != 0:
        raise LittleCheesemongerError("subprocess error")
