from __future__ import annotations
from attr_dict import AttrDict
from typing import *
from types import * 
from ..core import logging_tool, name as name_tools
from ..core.value_sharing import FolderDict_withLock
import importlib
import os
from collections import OrderedDict
from multiprocessing.managers import SyncManager
import multiprocessing as mp
import threading
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

    def Init(self) -> None: pass

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
    __thread_shared_values: FolderDict_withLock = None
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

    @property
    def thread_shared_values(self) -> FolderDict_withLock | None:
        return self.__thread_shared_values

    @thread_shared_values.setter
    def thread_shared_values(self, t_sv:FolderDict_withLock) -> None:
        """If called before process start, it will raise Error in the future."""
        self.__thread_shared_values = t_sv
    

    def set_thread_shared_values_to_all_apps(self, t_sv:FolderDict_withLock) -> None:
        """
        Set to `self` and `child_thread_apps`.
        You must call after the app process was started. 
        If called before process start, it will raise Error in the future.
        """
        self.thread_shared_values = t_sv
        for app in self.child_thread_apps.values():
            app.set_thread_shared_values_to_all_apps(t_sv)

    def _add_shared_value(self, obj_name:str, obj:Any ,for_thread:bool) -> None:
        """
        Add sharing object to shared_values.
        If for_thread is True, set to `thread_shared_values`,
        else `process_shared_values`.
        """
        name = name_tools.join(self.name, obj_name)
        if for_thread:
            self.thread_shared_values[name] = obj
        else:
            self.process_shared_values[name] = obj

    def addProcessSharedValue(self, obj_name:str, obj:Any) -> None:
        """Interface of `_add_shared_value`"""
        return self._add_shared_value(obj_name, obj,False)

    def addThreadSharedValue(self, obj_name:str, obj:Any) -> None:
        """Interface of `_add_shared_value`"""
        return self._add_shared_value(obj_name, obj,True)

    def RegisterProcessSharedValues(self, sync_manager: SyncManager) -> None:
        """Override function.
        Register value for sharing inter `multiprocessing`.
        You must call `super().RegisterProcessSharedValues` in your override
        because it calls `<child_app>.RegisterProcessSharedValues`.
        
        Usage:
            Please use `addProcessSharedValue` method to register a shared object.
            The object will be stored into `self.process_shared_values`.
            You can see other shared objects after process launched.


        Args:
            - sync_manager
                return value of `multiprocessing.Manager`.
                Please use it for sharing values.
        """
        for app in self.child_apps.values():
            app.RegisterProcessSharedValues(sync_manager)

    def RegisterThreadSharedValues(self) -> None:
        """Override function.
        Register value for sharing inter `threading`.
        You must call `super().RegisterProcessSharedValues` in your override
        because it calls `<child_app>.RegisterProcessSharedValues`.
        
        Usage:
            Please use `addThreadSharedValue` method to register a shared object.
            The object will be stored into `self.thread_shared_values`.
            You can see other shared objects after process launched.

        Args:
            Nothing.
        """

        for app in self.child_thread_apps.values():
            app.RegisterThreadSharedValues()

    def _get_shared_value(self, name:str, for_thread:bool) -> Any:
        """
        Get shared value from `process_shared_values` or `thread_shared_values`
        by specifying a name.
        If name prefix is `.`, count dot and go upstream only its count number.
        And search and pickup shared value using `name`.
        """
        if name_tools.count_head_sep(name) > 0:
            name = name_tools.join(self.name, name)
        
        if for_thread:
            return self.thread_shared_values[name]
        else:
            return self.process_shared_values[name]

    def getProcessSharedValue(self, name:str) -> Any:
        """Interface of `_get_shared_value(...,for_thread=False)`"""
        return self._get_shared_value(name, False)
        
    def getThreadSharedValue(self, name:str) -> Any:
        """Interface of `_get_shared_value(...,for_thread=True)`"""
        return self._get_shared_value(name, True)

    def prepare_for_launching_thread_apps(self):
        """ 
        Prepare for launching thread applcations.
        Set thread shared values among self and child thread apps.
        """
        if not self.is_thread: # Only *head* of threads.
            t_sv = FolderDict_withLock(sep=name_tools.SEP)
            self.set_thread_shared_values_to_all_apps(t_sv)
            self.RegisterThreadSharedValues()