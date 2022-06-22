import ctypes
import multiprocessing as mp
import os
import sys
from multiprocessing.sharedctypes import Synchronized
from typing import *

from attr_dict import AttrDict

from .apps import Launcher
from .constants import DEFAULT_ENGINE_CONFIG_FILE, SHUTDOWN_NAME
from .core import argument_parsers, logging_tool
from .core.config_tools import deep_update, dict2attr, read_json, read_toml
from .core.value_sharing import FolderDict_withLock, make_readonly

logger = logging_tool.getLogger(logging_tool.MAIN_LOGGER_NAME)


def run():
    """runs JE project."""
    parser = argument_parsers.at_running()
    args = parser.parse_args()

    project_dir = args.project_dir
    engine_config_file = args.engine_config_file
    config_file = args.config_file
    log_level = args.log_level

    # move to project directory and add it into path.
    os.chdir(project_dir)
    project_dir = os.getcwd()
    sys.path.insert(0, project_dir)

    # load engine config file.
    user_engine_config = read_toml(engine_config_file)
    user_engine_config["logging"]["log_level"] = log_level
    default_engine_config = read_toml(DEFAULT_ENGINE_CONFIG_FILE)
    user_engine_config = deep_update(default_engine_config, user_engine_config)
    engine_config = dict2attr(user_engine_config)

    # load config of the project.
    config = read_json(config_file)
    config = dict2attr(config)

    # logging
    logging_tool.setRootLoggerComponents(engine_config.logging)
    ### starting logging server
    logging_server = logging_tool.getLoggingServer(engine_config.logging)
    logging_server.start()

    # set process spawn method
    start_method = engine_config.multiprocessing.start_method
    mp.set_start_method(start_method)

    try:
        logger.info("JarvisEngine launch.")
        main_process(config, engine_config, project_dir)
    except BaseException as e:
        logger.exception(e)
    logging_server.shutdown()
    logger.info("JarvisEngine shutdown.")


def main_process(config: AttrDict, engine_config: AttrDict, project_dir: str) -> None:
    """main process"""
    mp.freeze_support()
    launcher = Launcher(config, engine_config, project_dir)
    with mp.Manager() as sync_manager:
        p_sv = launcher.prepare_for_launching(sync_manager)
        shutdown = create_shutdown(p_sv)
        launcher.launch(p_sv)
        wait_for_EnterKey(shutdown)
        launcher.join()


def create_shutdown(process_shared_values: FolderDict_withLock) -> Synchronized:
    """
    Creates a shutdown value and share it inter all app processes.
    The shared shutdown value is readonly.
    Returns pure shutdown value (writable).
    """
    shutdown = mp.Value(ctypes.c_bool, False)
    shutdown_read_only = make_readonly(shutdown)
    process_shared_values[SHUTDOWN_NAME] = shutdown_read_only
    return shutdown


def wait_for_EnterKey(shutdown: Synchronized) -> None:
    """Waiting for pushing enter key."""
    input()
    shutdown.value = True
