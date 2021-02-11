import os
import subprocess

import pytest
from click.testing import CliRunner

from little_cheesemonger._cli import entrypoint

PACKAGE_NAME = "example_package"
PACKAGE_VERSION = "1.0.0"
CUSTOM_LOADER_IMPORT_PATH = "tests.integration.assets.custom_loader.recipe_loader"


@pytest.fixture(autouse=True, scope="module")
def invoke_with_loader():

    result = CliRunner().invoke(
        entrypoint,
        [
            "--loader",
            CUSTOM_LOADER_IMPORT_PATH,
            "--loader-kwarg",
            f"package_name={PACKAGE_NAME}",
            "--loader-kwarg",
            f"package_version={PACKAGE_VERSION}",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    return result


def test_custom_loader__system_dependencies_installed():
    assert b"atlas.x86_64" in subprocess.check_output(["yum", "list", "installed"])


def test_custom_loader__python_dependencies_installed():
    for python_version in os.listdir("/opt/python"):
        assert b"nyancat" in subprocess.check_output(
            [f"/opt/python/{python_version}/bin/pip", "list"]
        )


def test_custom_loader__environment_variables_set():
    assert os.environ["FOO"] == "BAR"


def test_custom_loader__steps_run():
    assert b"foobar.txt" in subprocess.check_output(["ls", "/"])
