from JarvisEngine.apps import base_app

# prepare 
from JarvisEngine.core.config_tools import read_json, read_toml, dict2attr
from JarvisEngine.constants import DEFAULT_ENGINE_CONFIG_FILE
from JarvisEngine.core import logging_tool
from JarvisEngine.apps.launcher import to_project_config
import os
import sys
from JarvisEngine.core.value_sharing import FolderDict_withLock

PROJECT_DIR = "TestEngineProject"
sys.path.insert(0,os.path.join(os.getcwd(),PROJECT_DIR))
TEST_CONFIG_FILE_PATH = os.path.join(PROJECT_DIR,"config.json5")

project_config = dict2attr(read_json(TEST_CONFIG_FILE_PATH))
project_config = to_project_config(project_config)

engine_config = read_toml(DEFAULT_ENGINE_CONFIG_FILE)
engine_config["logging"]["log_level"] = "DEBUG"
engine_config = dict2attr(engine_config)

def _cd_project_dir(func):
    def cd(*args, **kwds):
        os.chdir(PROJECT_DIR)
        func(*args,**kwds)
        os.chdir("../")
    return cd

def _check_property_override(app, attr:str):
    try:
        setattr(app, attr, None)
        raise AssertionError(f"The property `{attr}` of {app} is overrided!")
    except AttributeError: pass

@_cd_project_dir
def test_import_app():
    
    path = "App0.app.App0"
    app_cls, mod = base_app.BaseApp.import_app(path)
    assert issubclass(app_cls, base_app.BaseApp)
    assert mod.__file__ == os.path.join(os.getcwd(), "App0","app.py")
    try:
        base_app.BaseApp.import_app("JarvisEngine.core.Logger")
        raise AssertionError
    except ImportError: pass
    

@_cd_project_dir
def test__init__():
    
    # test_properties():
    name = "MAIN.App1.App1_1"
    config = project_config.MAIN.apps.App1
    app_dir = "TestEngineProject/App1/App1_1"
    app = base_app.BaseApp(name, config, engine_config, project_config, app_dir)
    assert app.name == name
    assert app.config == config
    assert app.engine_config == engine_config
    assert app.project_config == project_config
    assert app.app_dir == app_dir
    assert isinstance(app.logger, logging_tool.Logger)

    _check_property_override(app, "name")
    _check_property_override(app, "config")
    _check_property_override(app, "engine_config")
    _check_property_override(app, "project_config")
    _check_property_override(app, "app_dir")
    _check_property_override(app, "logger")

    # test_set_config_attrs():
    name = "MAIN.App1"
    config = project_config.MAIN.apps.App1
    app_dir = "TestEngineProject/App1"
    app = base_app.BaseApp(name, config, engine_config, project_config, app_dir)

    assert app.module_name == config.path
    assert app.is_thread == config.thread
    assert app.child_app_configs == config.apps

    name = "MAIN.App0"
    config = project_config.MAIN.apps.App0
    app_dir = "TestEngineProject/App0"
    app = base_app.BaseApp(name, config, engine_config, project_config, app_dir)

    assert app.module_name == config.path
    assert app.is_thread == config.thread
    assert app.child_app_configs == base_app.AttrDict()

    # test construct_child_apps()
    name = "MAIN.App1"
    config = project_config.MAIN.apps.App1
    app_dir = os.path.join(os.getcwd(), "App1")
    app = base_app.BaseApp(name, config, engine_config, project_config, app_dir)

    assert "App1_1" in app.child_apps
    assert "App1_2" in app.child_apps
    App1_1, App1_2 = app.child_apps["App1_1"], app.child_apps["App1_2"]
    assert App1_1.name == "MAIN.App1.App1_1"
    assert App1_2.name == "MAIN.App1.App1_2"
    assert App1_1.module_name == "App1.App1_1.app.App1_1"
    assert App1_2.module_name == "App1.App1_2.app.App1_2"
    assert App1_1.is_thread == True
    assert App1_2.is_thread == False
    ### child_thread_apps
    assert "App1_1" in app.child_thread_apps
    assert "App1_2" not in app.child_thread_apps
    App1_1 = app.child_thread_apps["App1_1"]
    assert App1_1.is_thread == True

    ### child_process_apps
    assert "App1_1" not in app.child_process_apps
    assert "App1_2" in app.child_process_apps
    App1_2 = app.child_process_apps["App1_2"]
    assert App1_2.is_thread == False

    apps = config.apps
    assert App1_1.config == apps.App1_1
    assert App1_2.config == apps.App1_2
    assert App1_1.app_dir == os.path.join(app_dir, "App1_1")
    assert App1_2.app_dir == os.path.join(app_dir, "App1_2")

@_cd_project_dir
def test_process_shared_values():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    
    # Initial value is None
    assert MainApp.process_shared_values == None
    assert MainApp._process_shared_values == None
    App0 = MainApp.child_apps["App0"]
    App1 = MainApp.child_apps["App1"]
    assert App0.process_shared_values == None
    assert App1.process_shared_values == None

    fdwl= FolderDict_withLock(sep=".")

    MainApp.process_shared_values = fdwl
    assert MainApp.process_shared_values is fdwl
    assert MainApp._process_shared_values is fdwl
    assert App0.process_shared_values is fdwl
    assert App1.process_shared_values is fdwl
    App1_1 = App1.child_apps["App1_1"]
    App1_2 = App1.child_apps["App1_2"]

    assert App1_1.process_shared_values is fdwl
    assert App1_2._process_shared_values is fdwl