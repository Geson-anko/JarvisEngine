def test_import():
    # test logging tool
    import logging_server

    from JarvisEngine.core import Logger, LoggingServer

    assert LoggingServer is logging_server.LoggingServer
    assert Logger is logging_server.SocketLogger
