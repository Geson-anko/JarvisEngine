from JarvisEngine import apps

def test_import():
    from JarvisEngine.apps.base_app import BaseApp
    assert apps.BaseApp is BaseApp