import copy
import multiprocessing as mp
import os

# prepare
import time
from logging import INFO

from attr_dict import AttrDict

from JarvisEngine.apps import base_app
from JarvisEngine.core.logging_tool import getLoggingServer
from JarvisEngine.core.value_sharing import FolderDict_withLock

from .test_base_app import PROJECT_DIR
from .test_base_app import engine_config as src_ec
from .test_base_app import project_config

engine_config: AttrDict = copy.deepcopy(src_ec)
engine_config.logging.port = 20222
ls = getLoggingServer(engine_config.logging)
ls.start()


class cd_project_dir:
    def __enter__(self):
        os.chdir(PROJECT_DIR)

    def __exit__(self, *args):
        os.chdir("..")


def test_Init(caplog):
    name = "Launcher"
    config = project_config.Launcher
    app_dir = PROJECT_DIR
    with cd_project_dir():
        base_app.BaseApp(name, config, engine_config, project_config, app_dir)
        time.sleep(0.1)
        rec_tup = caplog.record_tuples
        assert ("Launcher.App0", INFO, "Init0") in rec_tup
        assert ("Launcher.App1", INFO, "Init1") in rec_tup
        assert ("Launcher.App1.App1_1", INFO, "Init1_1") in rec_tup
        assert ("Launcher.App1.App1_2", INFO, "Init1_2") in rec_tup


def test_RegisterProcessSharedValues():
    name = "Launcher"
    config = project_config.Launcher
    app_dir = PROJECT_DIR
    with mp.Manager() as shmm, cd_project_dir():
        MainApp = base_app.BaseApp(name, config, engine_config, project_config, app_dir)
        fdwl = FolderDict_withLock(sep=".")
        MainApp.set_process_shared_values_to_all_apps(fdwl)
        MainApp.RegisterProcessSharedValues(shmm)

        assert fdwl["Launcher.App1.int_value"] == 100
        assert fdwl["Launcher.App1.App1_2.float_value"] == 0.0
        assert fdwl["Launcher.App1.App1_1.str_value"] == "apple"
        assert fdwl["Launcher.App0.bool_value"] is True


def test_RegisterThreadSharedValues():
    name = "Launcher"
    config = project_config.Launcher
    app_dir = PROJECT_DIR
    with cd_project_dir():
        MainApp = base_app.BaseApp(name, config, engine_config, project_config, app_dir)
        fdwl = FolderDict_withLock(sep=".")
        MainApp.set_thread_shared_values_to_all_apps(fdwl)
        MainApp.RegisterThreadSharedValues()

        assert fdwl["Launcher.App0.set_obj"] == {"number"}
        assert fdwl["Launcher.App1.range_obj"] is None
        assert fdwl["Launcher.App1.App1_1.tuple_obj"] is None
        assert fdwl["Launcher.App1.App1_2.list_obj"] is None

        fdwl = FolderDict_withLock(sep=".")
        App1 = MainApp.child_apps["App1"]
        App1.set_thread_shared_values_to_all_apps(fdwl)
        App1.RegisterThreadSharedValues()
        assert fdwl["Launcher.App1.range_obj"] == range(10)
        assert fdwl["Launcher.App1.App1_1.tuple_obj"] == (True, False)
        assert fdwl["Launcher.App1.App1_2.list_obj"] is None
