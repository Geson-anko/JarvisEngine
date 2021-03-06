from JarvisEngine import constants
from JarvisEngine.core import config_tools


def test_default_engine_config():
    conf = config_tools.read_toml(constants.DEFAULT_ENGINE_CONFIG_FILE)
    assert "logging" in conf
    log_conf = conf["logging"]
    assert log_conf["host"] == "127.0.0.1"
    assert log_conf["port"] == 8316
    assert log_conf["message_format"] == "%(asctime)s.%(msecs)03d %(name)s [%(levelname)s]: %(message)s"
    assert log_conf["date_format"] == "%Y/%m/%d %H:%M:%S"

    assert "multiprocessing" in conf
    mp_conf = conf["multiprocessing"]
    assert mp_conf["start_method"] == "spawn"
