from JarvisEngine import apps


def test_import():
    from JarvisEngine.apps.base_app import BaseApp

    assert apps.BaseApp is BaseApp

    from JarvisEngine.apps.launcher import Launcher

    assert apps.Launcher == Launcher
