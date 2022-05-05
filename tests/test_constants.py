from JarvisEngine import constants

def test_ENGINE_PATH():
    import os
    assert os.path.join(os.getcwd(),"JarvisEngine") == constants.ENGINE_PATH
    assert os.path.isdir(constants.ENGINE_PATH)

def test_DEFAULT_CONFIG_FILE():
    import os
    assert os.path.join(os.getcwd(), "JarvisEngine/default_engine_config.toml") == constants.DEFAULT_ENGINE_CONFIG_FILE
    assert os.path.isfile(constants.DEFAULT_ENGINE_CONFIG_FILE)
