import copy
import subprocess

import pytest

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._run import (
    execute_steps,
    install_python_dependencies,
    install_system_dependencies,
    run,
    run_subprocess,
    set_environment_variables,
)
from tests.constants import ARCHITECTURE, PLATFORM, PYTHON_BINARIES, PYTHON_VERSION

ENVIRONMENT_VARIABLES = ["foo=bar"]
SYSTEM_DEPENDENCIES = ["foo-1.0.0"]
PYTHON_DEPENDENCIES = ["foo==1.0.0"]
STEPS = ["foo"]
CONFIGURATION = {
    "environment_variables": ENVIRONMENT_VARIABLES,
    "system_dependencies": SYSTEM_DEPENDENCIES,
    "python_dependencies": PYTHON_DEPENDENCIES,
    "steps": STEPS,
}


@pytest.fixture
def set_environment_variables_mock(mocker):
    return mocker.patch("little_cheesemonger._run.set_environment_variables")


@pytest.fixture
def install_system_dependencies_mock(mocker):
    return mocker.patch("little_cheesemonger._run.install_system_dependencies")


@pytest.fixture
def install_python_dependencies_mock(mocker):
    return mocker.patch("little_cheesemonger._run.install_python_dependencies")


@pytest.fixture
def execute_steps_mock(mocker):
    return mocker.patch("little_cheesemonger._run.execute_steps")


@pytest.fixture
def run_subprocess_mock(mocker):
    return mocker.patch("little_cheesemonger._run.run_subprocess")


@pytest.fixture
def get_python_binaries(mocker):
    return mocker.patch(
        "little_cheesemonger._run.get_python_binaries",
        return_value=PYTHON_BINARIES[ARCHITECTURE][PLATFORM],
    )


@pytest.fixture
def os_mock(mocker):
    return mocker.patch("little_cheesemonger._run.os")


@pytest.fixture
def subprocess_run_mock(mocker):
    return mocker.patch("little_cheesemonger._run.subprocess.run")


def test_run__environment_variables_set_in_configuration__set_environment_variables_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    run(CONFIGURATION)

    set_environment_variables_mock.assert_called_once_with(ENVIRONMENT_VARIABLES)


def test_run__environment_variables_not_set_in_configuration__set_environment_variables_not_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    configuration = copy.deepcopy(CONFIGURATION)
    configuration["environment_variables"] = None

    run(configuration)

    set_environment_variables_mock.assert_not_called()


def test_run__system_dependencies_set_in_configuration__install_system_dependencies_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    run(CONFIGURATION)

    install_system_dependencies_mock.assert_called_once_with(SYSTEM_DEPENDENCIES)


def test_run__system_dependencies_not_set_in_configuration__install_system_dependencies_not_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    configuration = copy.deepcopy(CONFIGURATION)
    configuration["system_dependencies"] = None

    run(configuration)

    install_system_dependencies_mock.assert_not_called()


def test_run__python_dependencies_set_in_configuration__install_python_dependencies_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    run(CONFIGURATION)

    install_python_dependencies_mock.assert_called_once_with(PYTHON_DEPENDENCIES)


def test_run__python_dependencies_not_set_in_configuration__install_python_dependencies_not_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    configuration = copy.deepcopy(CONFIGURATION)
    configuration["python_dependencies"] = None

    run(configuration)

    install_python_dependencies_mock.assert_not_called()


def test_run__steps_set_in_configuration__execute_steps_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    run(CONFIGURATION)

    execute_steps_mock.assert_called_once_with(STEPS)


def test_run__steps_not_set_in_configuration__execute_steps_not_called(
    set_environment_variables_mock,
    install_system_dependencies_mock,
    install_python_dependencies_mock,
    execute_steps_mock,
):

    configuration = copy.deepcopy(CONFIGURATION)
    configuration["steps"] = None

    run(configuration)

    execute_steps_mock.assert_not_called()


def test_set_environment_variables__os_environ_update_called(os_mock):

    expanded = {"foo": "bar"}

    set_environment_variables(ENVIRONMENT_VARIABLES)

    os_mock.environ.update.assert_called_once_with(expanded)


def test_set_environment_variables__raise_LittleCheesemongerError():

    with pytest.raises(LittleCheesemongerError, match=r"Unable to extract.*"):
        set_environment_variables("invalid")


def test_install_system_dependencies__run_subprocess_called_with_command(
    run_subprocess_mock,
):

    install_system_dependencies(SYSTEM_DEPENDENCIES)

    run_subprocess_mock.assert_called_once_with(
        ["yum", "install", "-y"] + SYSTEM_DEPENDENCIES
    )


def test_install_python_dependencies__run_subprocess_called_with_command(
    run_subprocess_mock, get_python_binaries
):

    install_python_dependencies(PYTHON_DEPENDENCIES)

    run_subprocess_mock.assert_called_once_with(
        [
            str(PYTHON_BINARIES[ARCHITECTURE][PLATFORM][PYTHON_VERSION] / "pip"),
            "install",
        ]
        + PYTHON_DEPENDENCIES
    )


def test_execute_steps__run_subprocess_called_with_commands(run_subprocess_mock):

    execute_steps(STEPS)

    run_subprocess_mock.assert_called_with(STEPS[0].split(" "))


def test_run_subprocess__subprocess_called_with_command(subprocess_run_mock):

    command = "command"

    run_subprocess(command)

    subprocess_run_mock.assert_called_once_with(command, check=True, shell=True)


def test_run_subprocess__return_code_is_not_zero__raise_LittleCheesemongerError(
    subprocess_run_mock,
):

    subprocess_run_mock.side_effect = subprocess.CalledProcessError(1, "command")

    with pytest.raises(LittleCheesemongerError, match=r"Subprocess error: ."):
        run_subprocess("command")
