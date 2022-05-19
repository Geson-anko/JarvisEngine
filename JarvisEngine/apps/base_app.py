from __future__ import annotations
from attr_dict import AttrDict
from typing import *
from types import * 
from ..core import logging_tool, name as name_tools
from ..core.value_sharing import FolderDict_withLock
import importlib
import os
from collections import OrderedDict

class BaseApp(object):
    """
    The base class of all applications in JarvisEngine.
    Attrs:
    - name: str
        The identical name among all applications.
        This is given by parent application.

    - child_apps: OrderedDict  
        The ordered dictionary that contains constructed child apps.
        self.child_apps["child_name"] -> child app

    - child_thread_apps: OrderedDict
        Contains child apps that are launched as a thread.
        They are `is_thread=True`.

    - child_process_apps: OrderedDict
        Contains child apps that are launched as a Process.
        They are `is_thread=False`.

    - logger: Logger
        The logger for multiprocessing logging.

    - config: AttrDict
        `config.json5` of under the application.

    - engine_config: AttrDict
        AttrDict of `engine_config.toml`
    
    - project_config: AttrDict
        Full of `config.json5`

    - app_dir: str | None
        The directory to the application.
    
    - module_name: str
        The import name of application.

    - is_thread: bool
        Whether the application is thread or process.

    - child_app_configs
        `apps` attribute of `self.config`.
    
    Override methods
    - Init()  
        called at end of `__init__`
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

        self.Init()

    def Init(self)-> NoReturn: pass

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
        self.child_thread_apps = OrderedDict()
        self.child_process_apps = OrderedDict()

        for child_name, child_conf in self.child_app_configs.items():
            ch_path:str = child_conf.path 
            
            full_child_name = name_tools.join(self.name, child_name)
            app_cls, mod = self.import_app(ch_path)
            app_dir = os.path.dirname(mod.__file__)

            child_app = app_cls(
                full_child_name, child_conf,self.engine_config,
                self.project_config, app_dir
            )
            self.child_apps[child_name] = child_app
            if child_app.is_thread:
                self.child_thread_apps[child_name] = child_app
            else:
                self.child_process_apps[child_name] = child_app

    @staticmethod
    def import_app(path:str) -> Tuple[BaseApp, ModuleType]:
        """import the application class.
        Args:
        - path: str
            The import name of app.
            `import <path>`
        
        return -> AppClass, Module

        If imported class is not subclass of BaseApp, 
        This method raises `ImportError`.
        """
        mod_name, cls_name= path.rsplit(".",1)
        mod = importlib.import_module(mod_name)
        app_cls = getattr(mod, cls_name)
        
        if issubclass(app_cls, BaseApp):
            return app_cls, mod
        else:
            raise ImportError(f"{path} is not a subclass of BaseApp!")

    __process_shared_values: FolderDict_withLock = None

    @property
    def process_shared_values(self) -> FolderDict_withLock | None:
        return self.__process_shared_values
    
    @process_shared_values.setter
    def process_shared_values(self, p_sv:FolderDict_withLock) -> None:
        self.__process_shared_values = p_sv
        
    def set_process_shared_values_to_all_apps(self, p_sv:FolderDict_withLock) -> None:
        """
        Set process shared value to `self` and `child_apps`
        Do not call if application process was started.
        """
        self.process_shared_values = p_sv
        for app in self.child_apps.values():
            app.set_process_shared_values_to_all_apps(p_sv)


