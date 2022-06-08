import multiprocessing as mp
import os
import threading
from multiprocessing.managers import SyncManager
from typing import *

from ..core import name as name_tools
from ..core.value_sharing import FolderDict_withLock
from .base_app import AttrDict, BaseApp

LAUNCHER_NAME = "Launcher"


def to_project_config(config: AttrDict) -> AttrDict:
    """convert `config` to `project_config`
    `project_config` has the following structure.
    ```
    {
        Launcher: {
            path: "JarvisEngine.apps.Launcher",
            thread: true,
            apps: config
        }

    }
    ```
    """
    pconf_dict = {LAUNCHER_NAME: {"path": "JarvisEngine.apps.Launcher", "thread": False, "apps": config}}
    project_config = AttrDict(pconf_dict)
    return project_config


class Launcher(BaseApp):
    """The origin of appcation processes."""

    def __init__(self, config: AttrDict, engine_config: AttrDict, project_dir: str) -> None:
        """Initialize Launcher.
        converts `config` to `project_config`, and sets name.
        """
        name = LAUNCHER_NAME
        project_config = to_project_config(config)
        config = project_config[name]
        super().__init__(name, config, engine_config, project_config, project_dir)

    def prepare_for_launching(self, sync_manager: SyncManager) -> FolderDict_withLock:
        """Prepare for launching.
        Returns Process Shared Values after registering shared values,
        and set None to Process Shared Values.
        """
        p_sv = FolderDict_withLock(sep=name_tools.SEP, lock=mp.RLock())
        self.set_process_shared_values_to_all_apps(p_sv)
        self.RegisterProcessSharedValues(sync_manager)
        self.set_process_shared_values_to_all_apps(None)
        return p_sv

    def launch(self, process_shared_values: FolderDict_withLock) -> None:
        """Launches all application processes/threads in background."""
        self.launcher_thread = threading.Thread(target=super().launch, name=self.name, args=(process_shared_values,))
        self.launcher_thread.start()

    def join(self):
        """Joins all application threads/processes."""
        self.launcher_thread.join()
