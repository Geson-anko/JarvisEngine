import argparse

from JarvisEngine import constants
from JarvisEngine.core import parsers


def _parse_args(parser: argparse.ArgumentParser, argv: list[str]) -> argparse.Namespace:
    return parser.parse_args(argv)


def test_at_launching():
    parser = parsers.at_launching()

    # test command
    args = _parse_args(parser, ["create"])
    assert args.command == "create"

    args = _parse_args(parser, ["run"])
    assert args.command == "run"

    try:
        _parse_args(parser, ["invalid command"])
        raise AssertionError("Invalid command was recognized!")
    except SystemExit:
        pass

    # test -ll, --log_level
    ### default behavior
    args = _parse_args(parser, ["create"])
    assert args.log_level == "DEBUG"

    ### run -ll INFO
    args = _parse_args(parser, ["run", "-ll", "INFO"])
    assert args.log_level == "INFO"

    ### run -ll=WARNING
    args = _parse_args(parser, ["run", "-ll=WARNING"])
    assert args.log_level == "WARNING"

    ### run --log_level ERROR
    args = _parse_args(parser, ["run", "--log_level", "ERROR"])
    assert args.log_level == "ERROR"

    ### create --log_level=CRITICAL
    args = _parse_args(parser, ["create", "--log_level=CRITICAL"])
    assert args.log_level == "CRITICAL"

    ### invalid option
    try:
        args = _parse_args(parser, ["create", "--log_level", "invalid log level"])
        raise AssertionError("Invalid option of `--log_level` is recognized!")
    except SystemExit:
        pass


def test_at_creating():
    parser = parsers.at_creating()

    argv = "create -d=bbb"
    args = _parse_args(parser, argv.split())
    assert args.creating_dir == "bbb"

    argv = "create --creating_dir ddd"
    args = _parse_args(parser, argv.split())
    assert args.creating_dir == "ddd"


def test_at_running():
    parser = parsers.at_running()

    # check default value
    argv = "run"
    args = _parse_args(parser, argv.split())
    assert args.project_dir == "./"
    assert args.config_file == constants.DEFAULT_CONFIG_FILE_NAME
    assert args.engine_config_file == constants.DEFAULT_ENGINE_CONFIG_FILE

    argv = "run -d=aaa"
    args = _parse_args(parser, argv.split())
    assert args.project_dir == "aaa"

    argv = "run --project_dir bbb"
    args = _parse_args(parser, argv.split())
    assert args.project_dir == "bbb"

    argv = "run -c aaa"
    args = _parse_args(parser, argv.split())
    assert args.config_file == "aaa"

    argv = "run --config_file=bbb"
    args = _parse_args(parser, argv.split())
    assert args.config_file == "bbb"

    argv = "run -ec aaa"
    args = _parse_args(parser, argv.split())
    assert args.engine_config_file == "aaa"

    argv = "run --engine_config_file bbb"
    args = _parse_args(parser, argv.split())
    assert args.engine_config_file == "bbb"
