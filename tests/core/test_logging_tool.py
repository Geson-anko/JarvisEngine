from JarvisEngine.core import logging_tool


def test_MAIN_LOGGER_NAME():
    assert logging_tool.MAIN_LOGGER_NAME == "MAIN"


def test_getLogger():
    import logging

    assert isinstance(logging_tool.getLogger(), logging.Logger)


def test_getAppLogger():
    class log_conf:
        log_level = "DEBUG"
        host = "127.0.0.1"
        port = 9999

    name = "aaa"
    logger = logging_tool.getAppLogger(name, log_conf)

    assert isinstance(logger, logging_tool.Logger)
    assert logger.level == log_conf.log_level
    assert logger.host == log_conf.host
    assert logger.port == log_conf.port
    assert logger.name == name


def test_setRootLoggerComponents():
    from JarvisEngine.constants import DEFAULT_ENGINE_CONFIG_FILE
    from JarvisEngine.core.config_tools import dict2attr, read_toml

    config = read_toml(DEFAULT_ENGINE_CONFIG_FILE)
    log_level = "DEBUG"
    config["logging"]["log_level"] = log_level
    log_conf = dict2attr(config).logging
    logging_tool.setRootLoggerComponents(log_conf)

    import logging

    root_logger = logging.getLogger()
    assert root_logger.level == logging._nameToLevel[log_level]
    assert root_logger.hasHandlers()
    hdlrs = root_logger.handlers[4:]  # ignore pytest handlers

    sh = hdlrs[0]
    assert isinstance(sh, logging.StreamHandler)
    assert sh.level == logging.NOTSET
    assert sh.formatter._fmt == log_conf.message_format
    assert sh.formatter.datefmt == log_conf.date_format


def test_getLoggingServer():
    class log_conf:
        host = "127.0.0.1"
        port = 8888

    server = logging_tool.getLoggingServer(log_conf)
    assert isinstance(server, logging_tool.LoggingServer)
    assert server.server_address == ("127.0.0.1", 8888)
