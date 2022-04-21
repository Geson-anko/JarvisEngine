from JarvisEngine import constants

def test_ENGINE_PATH():
    import os
    assert os.path.join(os.getcwd(),"JarvisEngine") == constants.ENGINE_PATH