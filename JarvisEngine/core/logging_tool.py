"""
This module provides useful tools for logging.

- LoggingServer
    Build a thread that manages log messages on the multiprocessing.
    The log messages are sent from SocketLogger.

- Logger
    SocketLogger, send log to LoggingServer.
    The name is changed to `Logger` in consideration of the case where
    SocketLogger will no longer be used in the future.
"""
from logging_server import LoggingServer, SocketLogger as Logger
import logging
from attr_dict import AttrDict
import sys

MAIN_LOGGER_NAME = "MAIN"

def getLogger(name:str = None) -> logging.Logger:
    """Return `logging.Logger`.
    This interface will be used for 
    adding default logger components.
    """
    return logging.getLogger(name)

def setRootLoggerComponents(log_conf:AttrDict) -> None:
    """Set components to root logger.
    Args:
    - log_conf:
        The config of logging (actually, `engine_config.logging`)
        This must have the following.
            - log_level:str
            - message_format:str
            - date_format:str

    Componentns:
    - StreamHandler (stdout)
    - set level.
    """
    log_level = log_conf.log_level
    msg_fmt = log_conf.message_format
    dt_fmt = log_conf.date_format

    root_logger = logging.getLogger()
    sh = logging.StreamHandler(sys.stdout)
    fmtter = logging.Formatter(msg_fmt,datefmt=dt_fmt)

    sh.setFormatter(fmtter)
    root_logger.addHandler(sh)
    root_logger.setLevel(log_level)


    

