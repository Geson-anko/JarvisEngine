from JarvisEngine.apps import launcher
from attr_dict import AttrDict
import importlib
from .test_base_app import (
    TEST_CONFIG_FILE_PATH,_cd_project_dir,engine_config
)
from JarvisEngine.core.config_tools import dict2attr, read_json
from JarvisEngine.core import logging_tool
import os
import multiprocessing as mp

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

@_cd_project_dir
def test_prepare_for_launching():
    lnchr = launcher.Launcher(config, engine_config,os.getcwd())
    with mp.Manager() as sync_manager:
        p_sv = lnchr.prepare_for_launching(sync_manager)

        assert lnchr.process_shared_values is None
        for app in lnchr.child_apps.values():
            assert app.process_shared_values is None
            for app2 in app.child_apps.values():
                assert app2.process_shared_values is None

        assert p_sv["MAIN.App1.int_value"] == 100
        assert p_sv["MAIN.App1.App1_2.float_value"] == 0.0
        assert p_sv["MAIN.App1.App1_1.str_value"] == "apple"
        assert p_sv["MAIN.App0.bool_value"] == True