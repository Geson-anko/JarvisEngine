from JarvisEngine.apps import base_app

# prepare 
from JarvisEngine.core.config_tools import read_json, read_toml, dict2attr
from JarvisEngine.constants import DEFAULT_ENGINE_CONFIG_FILE
from JarvisEngine.core import logging_tool
TEST_CONFIG_FILE_PATH = "TestEngineProject/config.json5"

project_config = dict2attr(read_json(TEST_CONFIG_FILE_PATH))

engine_config = read_toml(DEFAULT_ENGINE_CONFIG_FILE)
engine_config["logging"]["log_level"] = "DEBUG"
engine_config = dict2attr(engine_config)

def _check_property_override(app, attr:str):
    try:
        setattr(app, attr, None)
        raise AssertionError(f"The property `{attr}` of {app} is overrided!")
    except AttributeError: pass

def test_properties():
    name = "MAIN.App1.App1_1"
    config = project_config.App1
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

def test_set_config_attrs():
    name = "MAIN.App1"
    config = project_config.App1
    app_dir = "TestEngineProject/App1"
    app = base_app.BaseApp(name, config, engine_config, project_config, app_dir)
    app.set_config_attrs()

    assert app.module_name == config.path
    assert app.is_thread == config.thread
    assert app.child_app_configs == config.apps

    name = "MAIN.App0"
    config = project_config.App0
    app_dir = "TestEngineProject/App0"
    app = base_app.BaseApp(name, config, engine_config, project_config, app_dir)
    app.set_config_attrs()

    assert app.module_name == config.path
    assert app.is_thread == config.thread
    assert app.child_app_configs == base_app.AttrDict()