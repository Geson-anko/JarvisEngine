from JarvisEngine import constants


def test_ENGINE_PATH():
    import os

    assert os.path.join(os.getcwd(), "JarvisEngine") == constants.ENGINE_PATH
    assert os.path.isdir(constants.ENGINE_PATH)


def test_DEFAULT_CONFIG_FILE():
    import os

    assert (
        os.path.join(os.getcwd(), "JarvisEngine", "default_engine_config.toml") == constants.DEFAULT_ENGINE_CONFIG_FILE
    )
    assert os.path.isfile(constants.DEFAULT_ENGINE_CONFIG_FILE)


def test_DEFAULT_CONFIG_FILE_NAME():
    assert constants.DEFAULT_CONFIG_FILE_NAME == "config.json5"


def test_SHUTDOWN_NAME():
    assert constants.SHUTDOWN_NAME == "shutdown"
