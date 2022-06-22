import logging
from argparse import ArgumentParser

from ..constants import DEFAULT_CONFIG_FILE_NAME, DEFAULT_ENGINE_CONFIG_FILE

CREATE = "create"
RUN = "run"


def at_launching() -> ArgumentParser:
    """
    The parser used at lauching JarvisEngine.
    An Argument Parser class with the following options is returned.
        - command
            The running mode of JarvisEngine.
            If "create", Engine creates a project according to the template.
            If "run", Engine runs your project.

        - `-ll`,`--log_level`
            The log level when running JarvisEngine processes.
            The level names follow the standard python library logging.
    """
    parser = ArgumentParser()
    parser.add_argument("command", type=str, choices=[CREATE, RUN], help="Running mode of JarvisEngine")
    parser.add_argument(
        "-ll",
        "--log_level",
        type=str,
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="The log level when running JarvisEngine processes.",
    )

    return parser


def at_creating() -> ArgumentParser:
    """
    The parser used at creating JarvisEngine project.
    This returns an Argument Parser inherited
    `at_launching` and with the following options.
        - `-d`, `--creating_dir`
            The directory in which the project will be generated.
            If not provided, the project will be generated into the `os.getcwd()`.
    """
    parser = at_launching()
    parser.add_argument(
        "-d", "--creating_dir", type=str, default=".", help="The directory in which the project will be generated."
    )

    return parser


def at_running() -> ArgumentParser:
    """
    The parser used aat running JarvisEngine project.
    This returns an Arugment Parser inherited
    `at_launching` and with the following options.
        - `-d`, `--project_dir`
            The path to your project directory.
        - `-c`, `--config_file`
            The project config file name.
        - `-ec`, `--engine_config_file`
            The path to the engine config file.
    """
    parser = at_launching()
    parser.add_argument("-d", "--project_dir", type=str, default="./", help="The path to your project directory.")

    parser.add_argument(
        "-c", "--config_file", type=str, default=DEFAULT_CONFIG_FILE_NAME, help="The project config file name."
    )

    parser.add_argument(
        "-ec",
        "--engine_config_file",
        type=str,
        default=DEFAULT_ENGINE_CONFIG_FILE,
        help="The path to the engine config file.",
    )
    return parser
