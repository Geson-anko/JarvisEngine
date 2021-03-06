from __future__ import annotations

import importlib
import multiprocessing as mp
import os
import threading
import time
from collections import OrderedDict
from multiprocessing.managers import SyncManager
from types import *
from typing import *

from attr_dict import AttrDict

from ..constants import SHUTDOWN_NAME
from ..core import logging_tool
from ..core import name as name_tools
from ..core.value_sharing import FolderDictWithLock


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
        `config.json` of under the application.

    - engine_config: AttrDict
        AttrDict of `engine_config.toml`

    - project_config: AttrDict
        Full of `config.json`

    - app_dir: str | None
        The directory to the application.

    - module_name: str
        The import name of application.

    - is_thread: bool
        Whether the application is thread or process.

    - child_app_configs
        `apps` attribute of `self.config`.

    - frame_rate: float
        Period to call the `Update` method.
        The behavior depends on the value range.

        - frame_rate > 0.0
            Call `Update` method with that frame_rate

        - frame_rate == 0.0
            Call `Update` once and terminate immediately.

        - frame_rate < 0.0
            Call next `Update` immediately.

    - process_shared_values: FolderDictWithLock | None
        The property. Hold shard values inter `processes`.

    - thread_shared_values: FolderDictWithLock | None
        The property. Hold shared values inter `threads`.

    Override methods:

    - Init(self)
        Called at the end of `__init__`

    - RegisterProcessSharedValues(self, sync_manager)
        Register value for sharing inter `multiprocessing`.
        Called before the start of all application processes/threads.
        You must call `super().RegisterProcessSharedValues` in your override
        because it calls `<child_app>.RegisterProcessSharedValues`.

    - RegisterThreadSharedValues(self)
        Register value for sharing inter `threading`.
        Called at the begin of thread/process.
        You must call `super().RegisterProcessSharedValues` in your override
        because it calls `<child_app>.RegisterProcessSharedValues`.

    - Awake(self)
        Called at the begin of process/thread.

    - Start(self)
        Called at all applications are launched.

    - Update(self,delta_time)
        Called at intervals determined by `frame_rate` attribute.
        Args:
            - delta_time
                The elapsed time from previous frame.
    - End(self)
        Called at the end of process/thread.

    - Terminate(self)
        Called before the app terminate.
        If child applications could not be terminated,
        this method is never called.


    Application process flow:
        All methods are called in the following order.

    1. __init__
        1. set_config_attrs
        2. construct_child_apps
            1. import_app
        3. Init (override method)

    2. prepare_for_launching (only Launcher application.)
        1. set_process_shared_values_to_all_apps (set FolderDictWithLock)
        2. RegisterProcessSharedValues (override method)
            1. addProcessSharedValue
            2. RegisterProcessSharedValues (child applications)
                ...
        2. set_process_shared_values_to_all_apps (set None)

    3. launch (_launch)
        1. Awake (override method)
        2. setter of process_shared_value
        3. prepare_for_launching_thread_apps
            If process app
                1. set_thread_shared_values_to_all_apps(FolderDictWithLock)
                2. RegisterThreadSharedValues (override method)
                    1. RegisterThreadSharedValues (child thread apps)
                        ...
        4. launch_child_apps
        5. Start (override method)
        6. periodic_update
            1. Update (override method)
            2. adjust_update_frame_rate
            ...
        7. End (override method)
        8. join_child_apps
        9. Terminate (override method)
    """

    def __init__(
        self, name: str, config: AttrDict, engine_config: AttrDict, project_config: AttrDict, app_dir: str = None
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
        self.__config = config
        self.__engine_config = engine_config
        self.__project_config = project_config
        self.__app_dir = app_dir
        self.__logger = logging_tool.getAppLogger(name, engine_config.logging)

        self.set_config_attrs()

        self.construct_child_apps()

        self.Init()

    def Init(self) -> None:
        """Called at the end of `__init__`"""

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
    def app_dir(self) -> str:
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
        self.module_name: str = self.config.path
        self.is_thread: bool = self.config.thread

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
            ch_path: str = child_conf.path

            full_child_name = name_tools.join(self.name, child_name)
            app_cls, mod = self.import_app(ch_path)
            app_dir = os.path.dirname(mod.__file__)

            child_app = app_cls(full_child_name, child_conf, self.engine_config, self.project_config, app_dir)
            self.child_apps[child_name] = child_app
            if child_app.is_thread:
                self.child_thread_apps[child_name] = child_app
            else:
                self.child_process_apps[child_name] = child_app

    @staticmethod
    def import_app(path: str) -> Tuple[type, ModuleType]:
        """import the application class.
        Args:
        - path: str
            The import name of app.
            `import <path>`

        return -> AppClass, Module

        If imported class is not subclass of BaseApp,
        This method raises `ImportError`.
        """
        mod_name, cls_name = path.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        app_cls = getattr(mod, cls_name)

        if issubclass(app_cls, BaseApp):
            return app_cls, mod
        else:
            raise ImportError(f"{path} is not a subclass of BaseApp!")

    __process_shared_values: FolderDictWithLock = None
    __thread_shared_values: FolderDictWithLock = None

    @property
    def process_shared_values(self) -> FolderDictWithLock | None:
        return self.__process_shared_values

    @process_shared_values.setter
    def process_shared_values(self, p_sv: FolderDictWithLock) -> None:
        self.__process_shared_values = p_sv

    def set_process_shared_values_to_all_apps(self, p_sv: FolderDictWithLock) -> None:
        """
        Set process shared value to `self` and `child_apps`
        Do not call if application process was started.
        """
        self.process_shared_values = p_sv
        for app in self.child_apps.values():
            app.set_process_shared_values_to_all_apps(p_sv)

    @property
    def thread_shared_values(self) -> FolderDictWithLock | None:
        return self.__thread_shared_values

    @thread_shared_values.setter
    def thread_shared_values(self, t_sv: FolderDictWithLock) -> None:
        """If called before process start, it will raise Error in the future."""
        self.__thread_shared_values = t_sv

    def set_thread_shared_values_to_all_apps(self, t_sv: FolderDictWithLock) -> None:
        """
        Set to `self` and `child_thread_apps`.
        You must call after the app process was started.
        If called before process start, it will raise Error in the future.
        """
        self.thread_shared_values = t_sv
        for app in self.child_thread_apps.values():
            app.set_thread_shared_values_to_all_apps(t_sv)

    def _add_shared_value(self, obj_name: str, obj: Any, for_thread: bool) -> None:
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

    def addProcessSharedValue(self, obj_name: str, obj: Any) -> None:
        """Interface of `_add_shared_value`"""
        return self._add_shared_value(obj_name, obj, False)

    def addThreadSharedValue(self, obj_name: str, obj: Any) -> None:
        """Interface of `_add_shared_value`"""
        return self._add_shared_value(obj_name, obj, True)

    def RegisterProcessSharedValues(self, sync_manager: SyncManager) -> None:
        """Override function.
        Register value for sharing inter `multiprocessing`.
        Called before the start of all application processes/threads.
        You must call `super().RegisterProcessSharedValues` in your override
        because it calls `<child_app>.RegisterProcessSharedValues`.

        Usage:
            Please use `addProcessSharedValue` method to register a shared object.
            The object will be stored into `self.process_shared_values`.
            You can see other shared objects after process launched.

            Ex:
            >>> value = mp.Value("i")
            >>> self.addProcessSharedValue("int_value", value)

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
        Called at the begin of thread/process.
        You must call `super().RegisterProcessSharedValues` in your override
        because it calls `<child_app>.RegisterProcessSharedValues`.

        Usage:
            Please use `addThreadSharedValue` method to register a shared object.
            The object will be stored into `self.thread_shared_values`.
            You can see other shared objects after process launched.

            Ex:
            >>> self.addThreadProcessSharedValue("everything", context)

        Args:
            Nothing.
        """

        for app in self.child_thread_apps.values():
            app.RegisterThreadSharedValues()

    def _get_shared_value(self, name: str, for_thread: bool) -> Any:
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

    def getProcessSharedValue(self, name: str) -> Any:
        """Interface of `_get_shared_value(...,for_thread=False)`"""
        return self._get_shared_value(name, False)

    def getThreadSharedValue(self, name: str) -> Any:
        """Interface of `_get_shared_value(...,for_thread=True)`"""
        return self._get_shared_value(name, True)

    def prepare_for_launching_thread_apps(self):
        """
        Prepare for launching thread applications.
        Set thread shared values among self and child thread apps.
        """
        if not self.is_thread:  # Only *head* of threads.
            t_sv = FolderDictWithLock(sep=name_tools.SEP)
            self.set_thread_shared_values_to_all_apps(t_sv)
            self.RegisterThreadSharedValues()

    def launch_child_apps(self) -> None:
        """
        launch all child thread/process applications.
        """
        threads: List[threading.Thread] = []
        processes: List[mp.Process] = []

        for thread_app in self.child_thread_apps.values():
            thread = threading.Thread(
                target=thread_app.launch, name=thread_app.name, args=(self.process_shared_values,)
            )
            thread.start()
            threads.append(thread)

        for process_app in self.child_process_apps.values():
            process = mp.Process(target=process_app.launch, name=process_app.name, args=(self.process_shared_values,))
            process.start()
            processes.append(process)

        self.threads = threads
        self.processes = processes

    def join_child_apps(self) -> None:
        """
        Join all child thread/processes applications until they are terminated.
        """
        for thread in self.threads:
            thread.join()

        for process in self.processes:
            process.join()

    def _launch(self, process_shared_values: FolderDictWithLock) -> None:
        """
        Launch all applications as other threads or processes.
        """
        self.logger.info("launch")
        self.Awake()

        self.process_shared_values = process_shared_values
        self.prepare_for_launching_thread_apps()
        self.launch_child_apps()

        self.Start()

        self.periodic_update()

        self.End()

        self.join_child_apps()

        self.Terminate()
        self.logger.debug("terminate")

    def launch(self, process_shared_values: FolderDictWithLock) -> None:
        """
        Wrapps `self._launch` by try-except error catching.
        """
        try:
            self._launch(process_shared_values)
        except Exception as e:
            self.logger.exception(e)

    def Awake(self) -> None:
        """Called at begin of process/thread."""

    def Start(self) -> None:
        """Called at all applications are launched."""

    frame_rate = 0.0
    __start_time = float("-inf")

    @property
    def _update_start_time(self) -> float:
        return self.__start_time

    def adjust_update_frame_rate(self):
        """Adjusting frame rate of `Update` call."""
        wait_time = 1 / self.frame_rate - (time.time() - self.__start_time)
        if wait_time > 0:
            time.sleep(wait_time)
        self.__start_time = time.time()

    def periodic_update(self):
        """
        Calls override method `Update` at intervals determined by
        `frame_rate`, until shutdown.
        """
        shutdown = self.getProcessSharedValue(SHUTDOWN_NAME)
        self.logger.debug("periodic update")
        previous_time = time.time()
        self.__start_time = previous_time
        while not shutdown.value:
            current_time = time.time()
            self.Update(current_time - previous_time)
            previous_time = current_time

            if self.frame_rate == 0.0:
                # call `Update` once only when frame_rate is 0.
                break
            elif self.frame_rate > 0.0:
                self.adjust_update_frame_rate()
            else:
                # If the frame_rate is negative value,
                # the next `Update` method is called immediately.
                pass

    def Update(self, delta_time: float) -> None:
        """
        Called at intervals determined by `frame_rate` attribute.
        Args:
        - delta_time: float
            The interval time[seconds] of previous Update.
        """

    def End(self) -> None:
        """Called at the end of process/thread."""

    def Terminate(self) -> None:
        """
        Called before the app terminate.
        If child applications could not be terminated,
        this method is never called.
        """
