from JarvisEngine.apps import base_app

# prepare 
from JarvisEngine.core.config_tools import read_json, read_toml, dict2attr
from JarvisEngine.constants import DEFAULT_ENGINE_CONFIG_FILE
from JarvisEngine.core import logging_tool
from JarvisEngine.apps.launcher import to_project_config
import os
import sys
from JarvisEngine.core.value_sharing import FolderDict_withLock
import multiprocessing as mp

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
    App0 = MainApp.child_apps["App0"]
    App1 = MainApp.child_apps["App1"]
    assert App0.process_shared_values == None
    assert App1.process_shared_values == None

    fdwl= FolderDict_withLock(sep=".")

    MainApp.process_shared_values = fdwl 
    assert MainApp.process_shared_values is fdwl
    # Not set to child_apps.
    assert App0.process_shared_values == None 
    assert App1.process_shared_values == None
    App1_1 = App1.child_apps["App1_1"]
    App1_2 = App1.child_apps["App1_2"]

    assert App1_1.process_shared_values == None
    assert App1_2.process_shared_values == None

@_cd_project_dir
def test_set_process_shared_values_to_all_apps():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    
    fdwl= FolderDict_withLock(sep=".")
    MainApp.set_process_shared_values_to_all_apps(fdwl)
    assert MainApp.process_shared_values is fdwl
    App0 = MainApp.child_apps["App0"]
    App1 = MainApp.child_apps["App1"]
    App1_1 = App1.child_apps["App1_1"]
    App1_2 = App1.child_apps["App1_2"]

    assert App0.process_shared_values is fdwl
    assert App1.process_shared_values is fdwl
    assert App1_1.process_shared_values is fdwl
    assert App1_2.process_shared_values is fdwl

@_cd_project_dir
def test_thread_shared_values():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    
    # Initial values is None
    assert MainApp.thread_shared_values == None
    fdwl= FolderDict_withLock(sep=".")
    MainApp.thread_shared_values = fdwl
    assert MainApp.thread_shared_values is fdwl
    

@_cd_project_dir
def test_thread_shared_values():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    
    fdwl= FolderDict_withLock(sep=".")
    MainApp.set_thread_shared_values_to_all_apps(fdwl)
    assert MainApp.thread_shared_values is fdwl
    App0 = MainApp.child_thread_apps["App0"]
    App1 = MainApp.child_apps["App1"]
    App1_1 = App1.child_thread_apps["App1_1"]
    App1_2 = App1.child_apps["App1_2"]

    assert App0.thread_shared_values is fdwl
    assert App1.thread_shared_values is None
    assert App1_1.thread_shared_values is None # App1 is not thread
    assert App1_2.thread_shared_values is None

    App1_1.set_thread_shared_values_to_all_apps(fdwl)
    assert App1_1.thread_shared_values is fdwl 
    assert App1_2.thread_shared_values is None

@_cd_project_dir
def test__add_shared_value():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    
    fdwl_thread= FolderDict_withLock(sep=".")
    fdwl_process= FolderDict_withLock(sep=".")
    MainApp.set_process_shared_values_to_all_apps(fdwl_process)
    MainApp.set_thread_shared_values_to_all_apps(fdwl_thread)

    MainApp._add_shared_value("aaa", 10, for_thread=True)
    assert MainApp.thread_shared_values["MAIN.aaa"] == 10
    assert MainApp.process_shared_values["MAIN.aaa"] is None
    assert fdwl_thread["MAIN.aaa"] == 10

    MainApp._add_shared_value("bbb",20,for_thread=False)
    assert MainApp.thread_shared_values["MAIN.bbb"] is None
    assert MainApp.process_shared_values["MAIN.bbb"] == 20
    assert fdwl_process["MAIN.bbb"] == 20
    
@_cd_project_dir
def test_addProcessSharedValue():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    fdwl= FolderDict_withLock(sep=".")
    MainApp.process_shared_values = fdwl

    MainApp.addProcessSharedValue("ccc",30)
    MainApp.addProcessSharedValue("ddd",40)
    MainApp.addProcessSharedValue("eee",50)
    assert MainApp.process_shared_values["MAIN.ccc"] == 30
    assert MainApp.process_shared_values["MAIN.ddd"] == 40
    assert MainApp.process_shared_values["MAIN.eee"] == 50

@_cd_project_dir
def test_addThreadSharedValue():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    fdwl= FolderDict_withLock(sep=".")

    MainApp.thread_shared_values = fdwl 

    MainApp.addThreadSharedValue("fff",60)
    MainApp.addThreadSharedValue("ggg",70)
    MainApp.addThreadSharedValue("hhh",80)
    assert MainApp.thread_shared_values["MAIN.fff"] == 60
    assert MainApp.thread_shared_values["MAIN.ggg"] == 70
    assert MainApp.thread_shared_values["MAIN.hhh"] == 80

@_cd_project_dir
def test__get_shared_value():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    
    fdwl_thread= FolderDict_withLock(sep=".")
    fdwl_process= FolderDict_withLock(sep=".")
    MainApp.set_process_shared_values_to_all_apps(fdwl_process)
    MainApp.set_thread_shared_values_to_all_apps(fdwl_thread)

    App0 = MainApp.child_apps["App0"]
    App1 = MainApp.child_apps["App1"]
    App1_1 = App1.child_apps["App1_1"]
    App1_2 = App1.child_apps["App1_2"]
    # Process shared value
    MainApp.addProcessSharedValue("aaa",10)
    App0.addProcessSharedValue("bbb",True)
    App1.addProcessSharedValue("ccc", "apple")
    App1_1.addProcessSharedValue("ddd",1.0) 
    # Thread shared value
    MainApp.addThreadSharedValue("eee",False)
    App0.addThreadSharedValue("fff",20)

    assert MainApp._get_shared_value("MAIN.aaa",False) == 10
    assert MainApp._get_shared_value(".aaa",False) == 10
    assert MainApp._get_shared_value("MAIN.App0.bbb",False) == True
    assert App0._get_shared_value("..App1.ccc", False) == "apple"
    assert App1._get_shared_value(".App1_1.ddd",False) == 1.0
    
    assert MainApp._get_shared_value("..MAIN.eee",True) == False
    assert App0._get_shared_value("MAIN.App0.fff" ,True) == 20

@_cd_project_dir
def test_getProcessSharedValue():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    fdwl_process= FolderDict_withLock(sep=".")
    MainApp.set_process_shared_values_to_all_apps(fdwl_process)
    App0 = MainApp.child_apps["App0"]
    App1 = MainApp.child_apps["App1"]
    App1_1 = App1.child_apps["App1_1"]
    App1_2 = App1.child_apps["App1_2"]
    # Process shared value
    MainApp.addProcessSharedValue("aaa",10)
    App0.addProcessSharedValue("bbb",True)
    App1.addProcessSharedValue("ccc", "apple")
    App1_1.addProcessSharedValue("ddd",1.0) 


    assert MainApp.getProcessSharedValue("MAIN.aaa") == 10
    assert MainApp.getProcessSharedValue(".aaa") == 10
    assert MainApp.getProcessSharedValue("MAIN.App0.bbb") == True
    assert App0.getProcessSharedValue("..App1.ccc") == "apple"
    assert App1.getProcessSharedValue(".App1_1.ddd") == 1.0

@_cd_project_dir
def test_getThreadSharedValue():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    fdwl_thread= FolderDict_withLock(sep=".")
    MainApp.set_thread_shared_values_to_all_apps(fdwl_thread)

    App0 = MainApp.child_apps["App0"]

    # Thread shared value
    MainApp.addThreadSharedValue("eee",False)
    App0.addThreadSharedValue("fff",20)

    assert MainApp.getThreadSharedValue("..MAIN.eee") == False
    assert App0.getThreadSharedValue("MAIN.App0.fff") == 20

@_cd_project_dir
def test_prepare_for_launching_thread_apps():
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
    MainApp.prepare_for_launching_thread_apps()

    t_sv = MainApp.thread_shared_values
    assert isinstance(t_sv, FolderDict_withLock)
    assert t_sv["MAIN.App0.set_obj"] == {"number"}
    assert t_sv["MAIN.App1.range_obj"] is None

    App1 = MainApp.child_apps["App1"]
    App1.prepare_for_launching_thread_apps()
    t_sv = App1.thread_shared_values
    assert t_sv["MAIN.App1.range_obj"] == range(10)
    assert t_sv["MAIN.App1.App1_1.tuple_obj"] == (True, False)
    assert t_sv["MAIN.App1.App1_2.list_obj"] is None