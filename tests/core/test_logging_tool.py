from JarvisEngine.core import logging_tool

def test_MAIN_LOGGER_NAME():
    assert logging_tool.MAIN_LOGGER_NAME == "MAIN"
    
def test_getLogger():
    import logging
    assert isinstance(logging_tool.getLogger(), logging.Logger)
    