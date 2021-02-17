import logging

import pytest
from click.testing import CliRunner

from little_cheesemonger._cli import entrypoint, process_kwargs
from little_cheesemonger._errors import LittleCheesemongerError


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def log_level(caplog):
    caplog.set_level(logging.DEBUG)


@pytest.fixture(autouse=True)
def run(mocker):
    return mocker.patch("little_cheesemonger._cli.run")


def test_process_kwargs__return_dict():
    assert process_kwargs(("foo=bar", "baz=qux")) == {"foo": "bar", "baz": "qux"}


def test_process_kwargs__malformed_mapping_string__raise_LittleCheesemongerError():
    with pytest.raises(LittleCheesemongerError):
        process_kwargs(("invalid",))


def test_entrypoint__no_args(cli_runner):
    result = cli_runner.invoke(entrypoint, catch_exceptions=False)

    assert result.exit_code == 0


def test_entrypoint__custom_directory(cli_runner):
    result = cli_runner.invoke(entrypoint, ["my_directory"], catch_exceptions=False)

    assert result.exit_code == 0


def test_entrypoint__custom_loader(cli_runner):
    result = cli_runner.invoke(
        entrypoint, ["--loader", "my.custom.loader"], catch_exceptions=False
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_shorthand(cli_runner):
    result = cli_runner.invoke(
        entrypoint, ["-l", "my.custom.loader"], catch_exceptions=False
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_arg(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        ["--loader", "my.custom.loader", "--loader-arg", "baz"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_arg_shorthand(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        ["--loader", "my.custom.loader", "-l", "baz"],
        catch_exceptions=False,
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
        catch_exceptions=False,
    )

    assert result.exit_code == 0


def test_entrypoint__loader_args_without_custom_loader(cli_runner, caplog):
    result = cli_runner.invoke(
        entrypoint, ["--loader-arg", "baz"], catch_exceptions=False
    )

    assert result.exit_code == 1
    assert "Additional loader arguments can only" in caplog.text


def test_entrypoint__custom_loader_and_kwarg(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        ["--loader", "my.custom.loader", "--loader-kwarg", "baz=qux"],
        catch_exceptions=False,
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_and_kwarg_shorthand(cli_runner):
    result = cli_runner.invoke(
        entrypoint,
        ["--loader", "my.custom.loader", "-lk", "baz=qux"],
        catch_exceptions=False,
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
        catch_exceptions=False,
    )

    assert result.exit_code == 0


def test_entrypoint__loader_kwargs_without_custom_loader(cli_runner, caplog):
    result = cli_runner.invoke(
        entrypoint, ["--loader-kwarg", "baz=qux"], catch_exceptions=False
    )

    assert result.exit_code == 1
    assert "Additional loader arguments can only" in caplog.text


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
        catch_exceptions=False,
    )

    assert result.exit_code == 0


def test_entrypoint__custom_loader_error__exit_1_and_log_error(
    cli_runner,
    run,
):

    run.side_effect = LittleCheesemongerError

    result = cli_runner.invoke(
        entrypoint,
        [
            "--loader",
            "my.custom.loader",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
