
def test_import():
    # test logging tool
    from JarvisEngine.core import Logger,LoggingServer
    import logging_server
    assert LoggingServer is logging_server.LoggingServer
    assert Logger is logging_server.SocketLogger
