import os
import subprocess

import pytest
from click.testing import CliRunner

from little_cheesemonger._cli import entrypoint

PACKAGE_PATH = "./tests/integration/assets/example_package"


@pytest.fixture(autouse=True, scope="module")
def invoke_with_loader():

    result = CliRunner().invoke(entrypoint, [PACKAGE_PATH], catch_exceptions=False)

    assert result.exit_code == 0
    return result


def test_default_loader__system_dependencies_installed():
    assert b"atlas.x86_64" in subprocess.check_output(["yum", "list", "installed"])


def test_default_loader__python_dependencies_installed():
    for python_version in os.listdir("/opt/python"):
        assert b"nyancat" in subprocess.check_output(
            [f"/opt/python/{python_version}/bin/pip", "list"]
        )


def test_default_loader__environment_variables_set():
    assert os.environ["FOO"] == "BAR"


def test_default_loader__steps_run():
    assert b"foobar.txt" in subprocess.check_output(["ls", "/"])
