from .core import parsers, logging_tool
from .core.config_tools import read_toml, read_json, dict2attr, deep_update
import os
from attr_dict import AttrDict
from .constants import DEFAULT_ENGINE_CONFIG_FILE
from typing import *
import sys

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
    logger = logging_tool.getLogger(logging_tool.MAIN_LOGGER_NAME)
    
    try:
        logger.info("JarvisEngine launch.")
        main_process(config, engine_config, project_dir)
    except BaseException as e:
        logger.exception(e)
    
    logger.info("JarvisEngine shutdown.")
    
    
def main_process(config: AttrDict, engine_config:AttrDict, project_dir:str) -> NoReturn:
    """main process"""
