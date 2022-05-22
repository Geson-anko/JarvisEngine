from JarvisEngine.apps.base_app import BaseApp

# prepare 
import time
from JarvisEngine.core.logging_tool import getLoggingServer
from JarvisEngine.core.value_sharing import FolderDict_withLock
from JarvisEngine.apps.launcher import Launcher
from .test_base_app import (
    project_config, engine_config,PROJECT_DIR
)
from logging import INFO, WARNING
import os
import copy
import multiprocessing as mp

engine_config = copy.deepcopy(engine_config)
engine_config.logging.port = 20223
ls = getLoggingServer(engine_config.logging)
ls.start()

class cd_project_dir:
    def __enter__(self):
        os.chdir(PROJECT_DIR)
    def __exit__(self, *args):
        os.chdir("..")

def test_launch(caplog):
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    with cd_project_dir(), mp.Manager() as sync_manager:
        MainApp = BaseApp(name, config, engine_config, project_config,app_dir)
        p_sv = Launcher.prepare_for_launching(MainApp, sync_manager)
        MainApp.launch(p_sv)
        time.sleep(0.1)
        rec_tup = caplog.record_tuples

        assert ("MAIN", INFO, "launch") in rec_tup
        assert ("MAIN.App0", INFO, "launch") in rec_tup
        assert ("MAIN.App1", INFO, "launch") in rec_tup
        assert ("MAIN.App1.App1_1", INFO, "launch") in rec_tup
        assert ("MAIN.App1.App1_2", INFO, "launch") in rec_tup
        
    for record in caplog.records:
        assert record.levelno < WARNING, record.message
