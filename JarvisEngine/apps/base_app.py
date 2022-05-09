from __future__ import annotations
from attr_dict import AttrDict
from folder_dict import FolderDict
from typing import *
from ..core import logging_tool, name as name_tools
import importlib
import os
from collections import OrderedDict

class BaseApp(object):
    """
    The base class of all applications in JarvisEngine.
    """


    def __init__(
        self, name:str, config:AttrDict, engine_config:AttrDict, 
        project_config:AttrDict, app_dir:str = None
    ) -> None:
        """Initialization of BaseApp
        Args:
        - name
            The name of this application, is given by 
            its parent application.

        - config
            The config of the application.
            This have the following attributes.
            - path:str
                The import name of its app.
            - thread:bool
                Whether its App is thread or process.
            - apps (optional)
                Children app configs of the application.

        - engine_config
            The launching configuration of JarvisEngine.
            Please see `JarvisEngine/default_engine_config.toml`

        - project_config
            The whole configuration of applications.

        - app_dir (optional)
            The absolute path to the application folder.
        """
        self.__name = name
        self.__config  = config
        self.__engine_config = engine_config
        self.__project_config = project_config
        self.__app_dir = app_dir
        self.__logger = logging_tool.getAppLogger(name,engine_config.logging)
        
        self.set_config_attrs()

        self.construct_child_apps()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def config(self) -> AttrDict:
        return self.__config

    @property
    def engine_config(self) -> AttrDict:
        return self.__engine_config
    
    @property
    def project_config(self) -> AttrDict:
        return self.__project_config

    @property
    def app_dir(self) -> str or None:
        return self.__app_dir

    @property
    def logger(self) -> logging_tool.Logger:
        return self.__logger

    def set_config_attrs(self) -> None:
        """set config attrs to self.
        - module_name: str
            The import name of the application.            
        - is_thread: bool
            Whether the App is thread or process.
        - child_app_configs: 
            Child app configs of the application.
        """
        self.module_name:str = self.config.path
        self.is_thread:bool = self.config.thread

        if hasattr(self.config, "apps"):
            self.child_app_configs = self.config.apps
        else:
            self.child_app_configs = AttrDict()    

    def construct_child_apps(self):
        """Construct child applications of this.
        you can see constructed child apps 
        by `self.child_apps` attribute.
        """
        self.child_apps = OrderedDict()
        for child_name, child_conf in self.child_app_configs.items():
            ch_path:str = child_conf.path 
            
            full_child_name = name_tools.join(self.name, child_name)
            mod_name, cls_name = ch_path.rsplit(".",1)
            mod = importlib.import_module(mod_name)
            app_cls:BaseApp = getattr(mod,cls_name)
            app_dir = os.path.dirname(mod.__file__)

            child_app = app_cls(
                full_child_name, child_conf,self.engine_config,
                self.project_config, app_dir
            )
            self.child_apps[child_name] = child_app
        