from JarvisEngine import constants

def test_ENGINE_PATH():
    import os
    assert os.path.join(os.getcwd(),"JarvisEngine") == constants.ENGINE_PATH

def test_DEFAULT_CONFIG_FILE():
    import os
    assert os.path.join(os.getcwd(), "JarvisEngine/default_config.toml") == constants.DEFAULT_CONFIG_FILE