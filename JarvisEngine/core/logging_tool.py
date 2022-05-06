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

MAIN_LOGGER_NAME = "MAIN"

def getLogger(name:str = None) -> logging.Logger:
    """Return `logging.Logger`.
    This interface will be used for 
    adding default logger components.
    """
    return logging.getLogger(name)
