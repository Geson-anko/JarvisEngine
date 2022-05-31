from JarvisEngine.apps.base_app import BaseApp

# prepare 
import time
from JarvisEngine.run_project import create_shutdown
from JarvisEngine.core.logging_tool import getLoggingServer
from JarvisEngine.core.value_sharing import FolderDict_withLock
from JarvisEngine.apps.launcher import Launcher
from JarvisEngine.constants import SHUTDOWN_NAME
from .test_base_app import (
    project_config, engine_config,PROJECT_DIR
)
from logging import DEBUG, INFO, WARNING
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
    name = "Launcher"
    config = project_config.Launcher
    app_dir = PROJECT_DIR
    with cd_project_dir(), mp.Manager() as sync_manager:
        #MainApp = BaseApp(name, config, engine_config, project_config,app_dir)        
        #p_sv = Launcher.prepare_for_launching(MainApp, sync_manager)
        #MainApp.launch(p_sv)
        LauncherApp = Launcher(config.apps,engine_config,app_dir)
        p_sv = LauncherApp.prepare_for_launching(sync_manager)
        shutdown = create_shutdown(p_sv)
        LauncherApp.launch(p_sv)
        time.sleep(1.0)
        shutdown.value = True
        LauncherApp.join()
        time.sleep(0.1)
        rec_tup = caplog.record_tuples

        # launch
        assert ("Launcher", INFO, "launch") in rec_tup
        assert ("Launcher.App0", INFO, "launch") in rec_tup
        assert ("Launcher.App1", INFO, "launch") in rec_tup
        assert ("Launcher.App1.App1_1", INFO, "launch") in rec_tup
        assert ("Launcher.App1.App1_2", INFO, "launch") in rec_tup
        
        # Awake
        assert ("Launcher.App0", INFO, "Awake") in rec_tup
        assert ("Launcher.App1", INFO, "Awake") in rec_tup
        assert ("Launcher.App1.App1_1", INFO, "Awake") in rec_tup
        assert ("Launcher.App1.App1_2", INFO, "Awake") in rec_tup

        # Start
        assert ("Launcher.App0", INFO, "Start") in rec_tup
        assert ("Launcher.App1", INFO, "Start") in rec_tup
        assert ("Launcher.App1.App1_1", INFO, "Start") in rec_tup
        assert ("Launcher.App1.App1_2", INFO, "Start") in rec_tup

        # periodic_update
        assert ("Launcher", DEBUG, "periodic update") in rec_tup
        assert ("Launcher.App0", DEBUG, "periodic update") in rec_tup
        assert ("Launcher.App1", DEBUG, "periodic update") in rec_tup
        assert ("Launcher.App1.App1_1", DEBUG, "periodic update") in rec_tup
        assert ("Launcher.App1.App1_2", DEBUG, "periodic update") in rec_tup

        # Update
        ### called only once.
        assert ("Launcher.App0", INFO, "Update") in rec_tup
        assert rec_tup.count(("Launcher.App0", INFO, "Update")) == 1

        ### updating in 5 fps.
        assert ("Launcher.App1", INFO, "Update") in rec_tup
        assert 6 >= rec_tup.count(("Launcher.App1", INFO, "Update")) >= 4 

        ### updating in 10 fps.
        assert ("Launcher.App1.App1_1", INFO, "Update") in rec_tup
        assert 11 >= rec_tup.count(("Launcher.App1.App1_1", INFO, "Update")) >= 9

        ### updating in infinity fps. logged only 5 times
        assert rec_tup.count(("Launcher.App1.App1_2", INFO, "Update")) == 5

        # End
        assert ("Launcher.App0", INFO, "End") in rec_tup
        assert ("Launcher.App1", INFO, "End") in rec_tup
        assert ("Launcher.App1.App1_1", INFO, "End") in rec_tup
        assert ("Launcher.App1.App1_2", INFO, "End") in rec_tup

        # Terminate (override method)
        assert ("Launcher.App0", INFO, "Terminate.") in rec_tup
        assert ("Launcher.App1", INFO, "Terminate.") in rec_tup
        assert ("Launcher.App1.App1_1", INFO, "Terminate.") in rec_tup
        assert ("Launcher.App1.App1_2", INFO, "Terminate.") in rec_tup

        # terminate
        assert("Launcher", DEBUG, "terminate") in rec_tup
        assert("Launcher.App0", DEBUG, "terminate") in rec_tup
        assert("Launcher.App1", DEBUG, "terminate") in rec_tup
        assert("Launcher.App1.App1_1", DEBUG, "terminate") in rec_tup
        assert("Launcher.App1.App1_2", DEBUG, "terminate") in rec_tup

    for record in caplog.records:
        assert record.levelno < WARNING, record.message
