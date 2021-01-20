import logging

import pytest
from click.testing import CliRunner

from little_cheesemonger._cli import entrypoint


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_entrypoint__no_args(cli_runner):
    result = cli_runner.invoke(entrypoint)

    assert result.exit_code == 0


def test_entrypoint__custom_directory(cli_runner):
    result = cli_runner.invoke(entrypoint, ["my_directory"])

    assert result.exit_code == 0


def test_entrypoint__debug_not_set__log_level_set_to_WARNING(cli_runner):

    result = cli_runner.invoke(entrypoint)

    assert logging.getLogger("little_cheesemonger").level == logging.WARNING
    assert result.exit_code == 0


def test_entrypoint__debug_set__log_level_set_to_DEBUG(cli_runner):

    result = cli_runner.invoke(entrypoint, ["--debug"])

    assert logging.getLogger("little_cheesemonger").level == logging.DEBUG
    assert result.exit_code == 0


def test_entrypoint__custom_data_loader(cli_runner):
    result = cli_runner.invoke(entrypoint, ["--data-loader", "foo.py:bar"])

    assert result.exit_code == 0


def test_entrypoint__custom_data_loader_shorthand(cli_runner):
    result = cli_runner.invoke(entrypoint, ["-dl", "foo.py:bar"])

    assert result.exit_code == 0


def test_entrypoint__custom_data_loader_and_arg(cli_runner):
    result = cli_runner.invoke(
        entrypoint, ["--data-loader", "foo.py:bar", "--data-loader-arg", "baz"]
    )

    assert result.exit_code == 0


def test_entrypoint__custom_data_loader_and_arg_shorthand(cli_runner):
    result = cli_runner.invoke(
        entrypoint, ["--data-loader", "foo.py:bar", "-dl", "baz"]
    )

    assert result.exit_code == 0


def test_entrypoint__custom_data_loader_and_multiple_args(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        [
            "--data-loader",
            "foo.py:bar",
            "--data-loader-arg",
            "baz",
            "--data-loader-arg",
            "qux",
        ],
    )

    assert result.exit_code == 0


def test_entrypoint__data_loader_args_without_custom_loader(cli_runner):
    result = cli_runner.invoke(entrypoint, ["--data-loader-arg", "baz"])

    assert result.exit_code == 1
