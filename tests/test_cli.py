import logging

import pytest
from click.testing import CliRunner

from little_cheesemonger._cli import _process_kwargs, entrypoint
from little_cheesemonger._errors import LittleCheesemongerError


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def default_loader(mocker):
    return mocker.patch("little_cheesemonger._cli.default_loader")


@pytest.fixture(autouse=True)
def run(mocker):
    return mocker.patch("little_cheesemonger._cli.run")


def test_process_kwargs__return_dict():
    assert _process_kwargs(("foo=bar", "baz=qux")) == {"foo": "bar", "baz": "qux"}


def test_process_kwargs__malformed_mapping_string__raise_LittleCheesemongerError():
    with pytest.raises(LittleCheesemongerError):
        _process_kwargs(("invalid",))


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


def test_entrypoint__custom_loader(cli_runner):
    result = cli_runner.invoke(entrypoint, ["--loader", "my.custom.loader"])

    assert result.exit_code == 0


def test_entrypoint__custom_loader_shorthand(cli_runner):
    result = cli_runner.invoke(entrypoint, ["-l", "my.custom.loader"])

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_arg(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        ["--loader", "my.custom.loader", "--loader-arg", "baz"],
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_arg_shorthand(cli_runner):
    result = cli_runner.invoke(
        entrypoint, ["--loader", "my.custom.loader", "-l", "baz"]
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_multiple_args(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        [
            "--loader",
            "my.custom.loader",
            "--loader-arg",
            "baz",
            "--loader-arg",
            "qux",
        ],
    )

    assert result.exit_code == 0


def test_entrypoint__loader_args_without_custom_loader(cli_runner):
    result = cli_runner.invoke(entrypoint, ["--loader-arg", "baz"])

    assert result.exit_code == 1


def test_entrypoint__custom_loader_and_kwarg(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        ["--loader", "my.custom.loader", "--loader-kwarg", "baz=qux"],
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_kwarg_shorthand(cli_runner):
    result = cli_runner.invoke(
        entrypoint, ["--loader", "my.custom.loader", "-lk", "baz=qux"]
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_multiple_kwargs(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        [
            "--loader",
            "my.custom.loader",
            "--loader-kwarg",
            "foo=bar",
            "--loader-kwarg",
            "baz=qux",
        ],
    )

    assert result.exit_code == 0


def test_entrypoint__loader_kwargs_without_custom_loader(cli_runner):
    result = cli_runner.invoke(entrypoint, ["--loader-kwarg", "baz=qux"])

    assert result.exit_code == 1


def test_entrypoint__loader_with_arg_and_kwarg(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        [
            "--loader",
            "my.custom.loader",
            "--loader-arg",
            "foo",
            "--loader-kwarg",
            "baz=qux",
        ],
    )

    assert result.exit_code == 0
