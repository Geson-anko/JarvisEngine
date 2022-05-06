from attr_dict import AttrDict
from folder_dict import FolderDict
from typing import *
from ..core import logging_tool

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