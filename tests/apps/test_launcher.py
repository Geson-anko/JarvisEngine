from JarvisEngine.apps import launcher
from attr_dict import AttrDict
import importlib
from .test_base_app import (
    TEST_CONFIG_FILE_PATH,_cd_project_dir,engine_config
)
from JarvisEngine.core.config_tools import dict2attr, read_json
from JarvisEngine.core import logging_tool
import os
config = dict2attr(read_json(TEST_CONFIG_FILE_PATH))
project_config = launcher.to_project_config(config)

def test_to_project_config():
    config = AttrDict()
    proj_conf = launcher.to_project_config(config)
    assert "MAIN" in proj_conf
    launcher_conf = proj_conf.MAIN
    assert launcher_conf.path == "JarvisEngine.apps.Launcher"
    mod, app = launcher_conf.path.rsplit(".",1)
    assert getattr(importlib.import_module(mod), app) == launcher.Launcher
    assert launcher_conf.thread == True
    assert isinstance(launcher_conf.apps, AttrDict)
    assert launcher_conf.apps == config

@_cd_project_dir
def test__init__():
    lnchr = launcher.Launcher(config, engine_config,os.getcwd())
    assert lnchr.name == logging_tool.MAIN_LOGGER_NAME
    assert lnchr.config == project_config[logging_tool.MAIN_LOGGER_NAME]
    assert lnchr.project_config == project_config
    assert lnchr.app_dir == os.getcwd()