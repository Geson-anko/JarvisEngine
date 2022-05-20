from JarvisEngine.apps import base_app

# prepare
import time
from JarvisEngine.core.logging_tool import getLoggingServer
from .test_base_app import (
    project_config, engine_config,PROJECT_DIR
)
from logging import INFO
import os
import copy

engine_config = copy.deepcopy(engine_config)
engine_config.logging.port = 20222
ls = getLoggingServer(engine_config.logging)
ls.start()

class cd_project_dir:
    def __enter__(self):
        os.chdir(PROJECT_DIR)
    def __exit__(self, *args):
        os.chdir("..")

        
def test_Init(caplog):
    name = "MAIN"
    config = project_config.MAIN
    app_dir = PROJECT_DIR
    with cd_project_dir():
        MainApp = base_app.BaseApp(name, config, engine_config,project_config,app_dir)
        time.sleep(0.1)
        rec_tup = caplog.record_tuples
        assert ("MAIN.App0",INFO, "Init0") in rec_tup
        assert ("MAIN.App1",INFO, "Init1") in rec_tup
        assert ("MAIN.App1.App1_1",INFO, "Init1_1") in rec_tup
        assert ("MAIN.App1.App1_2",INFO, "Init1_2") in rec_tup
