from .base_app import BaseApp, AttrDict
from typing import *
import os
from ..core import logging_tool

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
            "thread": True,
            "apps": config
        }
    }
    project_config = AttrDict(pconf_dict)
    return project_config

class Launcher(BaseApp):
    """The origin of appcation processes.

    """

    def __init__(
        self, name: str, config: AttrDict, 
        engine_config: AttrDict, project_config:AttrDict
    ) -> None:
        super().__init__(name, config, engine_config, project_config, os.path.dirname(__file__))
