from .base_app import BaseApp, AttrDict
from typing import *
import os

class Launcher(BaseApp):
    """The origin of appcation processes.
    
    """

    def __init__(
        self, name: str, config: AttrDict, 
        engine_config: AttrDict, project_config:AttrDict
    ) -> None:
        super().__init__(name, config, engine_config, project_config, os.path.dirname(__file__))

