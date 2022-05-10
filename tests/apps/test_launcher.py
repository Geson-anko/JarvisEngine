from JarvisEngine.apps import launcher
from attr_dict import AttrDict
import importlib

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
