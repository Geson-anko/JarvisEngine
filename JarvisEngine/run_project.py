from .core import parsers, logging_tool
from .core.config_tools import read_toml, read_json, dict2attr, deep_update
import os
from attr_dict import AttrDict
from .constants import DEFAULT_ENGINE_CONFIG_FILE, SHUTDOWN_NAME
from typing import *
import sys
from .apps import Launcher
import multiprocessing as mp
from multiprocessing.sharedctypes import Synchronized
from .core.value_sharing import make_readonly, FolderDict_withLock
import ctypes
from pynput import keyboard
import time

logger = logging_tool.getLogger(logging_tool.MAIN_LOGGER_NAME)

def run():
    """runs JE project."""
    parser = parsers.at_running()
    args = parser.parse_args()

    project_dir = args.project_dir
    engine_config_file = args.engine_config_file
    config_file = args.config_file
    log_level = args.log_level

    # move to project directory and add it into path.
    os.chdir(project_dir)
    project_dir = os.getcwd()
    sys.path.insert(0,project_dir)

    # load engine config file.
    engine_config = read_toml(engine_config_file)
    engine_config["logging"]["log_level"] = log_level
    default_engine_config = read_toml(DEFAULT_ENGINE_CONFIG_FILE)
    engine_config = deep_update(default_engine_config, engine_config)
    engine_config = dict2attr(engine_config)

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
    
    
def main_process(config: AttrDict, engine_config:AttrDict, project_dir:str) -> NoReturn:
    """main process"""
    mp.freeze_support()
    launcher = Launcher(config, engine_config, project_dir)
    with mp.Manager() as sync_manager:
        p_sv = launcher.prepare_for_launching(sync_manager)
        shutdown = create_shutdown(p_sv)
        launcher.launch(p_sv)
        wait_for_QuitKeyboardCommand(shutdown,engine_config.commands.keyboard)
        launcher.join()

def create_shutdown(process_shared_values:FolderDict_withLock) -> Synchronized:
    """
    Creates a shutdown value and share it inter all app processes.
    The shared shutdown value is readonly.
    Returns pure shutdown value (writable).
    """
    shutdown = mp.Value(ctypes.c_bool, False)
    shutdown_read_only = make_readonly(shutdown)
    process_shared_values[SHUTDOWN_NAME] = shutdown_read_only
    return shutdown

def wait_for_QuitKeyboardCommand(shutdown:Synchronized, keyboard_command_config:AttrDict) -> None:
    """Waiting for quit keyboard command."""
    def on_activate():
        shutdown.value = True

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    quit_hot_key = keyboard_command_config.shutdown
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse(quit_hot_key),
        on_activate
    )

    listener = keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    )
    listener.start()
    
    while not shutdown.value:
        time.sleep(0.5)
