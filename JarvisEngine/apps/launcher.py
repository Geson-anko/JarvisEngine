from .base_app import BaseApp, AttrDict
from typing import *
import os
from ..core import logging_tool ,name as name_tools
from ..core.value_sharing import FolderDict_withLock
import multiprocessing as mp
from multiprocessing.managers import SyncManager


def to_project_config(config:AttrDict) -> AttrDict:
    """convert `config` to `project_config`
    `project_config` has the following structure.
    ```
    {
        MAIN: {
            path: "JarvisEngine.apps.Launcher",
            thread: true,
            apps: config
        }

    }
    ```
    """
    pconf_dict = {
        logging_tool.MAIN_LOGGER_NAME:{
            "path": "JarvisEngine.apps.Launcher",
            "thread": False,
            "apps": config
        }
    }
    project_config = AttrDict(pconf_dict)
    return project_config

class Launcher(BaseApp):
    """The origin of appcation processes.

    """

    def __init__(self, config: AttrDict, engine_config: AttrDict, project_dir:str) -> None:
        """Initialize Launcher.
        converts `config` to `project_config`, and sets name.
        """
        name = logging_tool.MAIN_LOGGER_NAME
        project_config = to_project_config(config)
        config = project_config[name]
        super().__init__(name, config, engine_config, project_config, project_dir)

    def prepare_for_launching(self, sync_manager:SyncManager) -> FolderDict_withLock:
        """ Prepare for launching.
        Returns Process Shared Values after registering shared values,
        and set None to Process Shared Values. 
        """
        p_sv = FolderDict_withLock(sep=name_tools.SEP, lock=mp.RLock())
        self.set_process_shared_values_to_all_apps(p_sv)
        self.RegisterProcessSharedValues(sync_manager)
        self.set_process_shared_values_to_all_apps(None)
        return p_sv