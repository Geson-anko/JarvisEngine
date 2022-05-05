from JarvisEngine.core import config_tools

def test_read_toml():
    conf = config_tools.read_toml("tests/core/config.toml")
    assert conf["title"] == "TOML Example"
    
    database = conf["database"]
    assert database["server"] == "192.168.1.1"
    assert database["ports"] == [ 8000, 8001, 8002 ]
    assert database["connection_max"] == 5000
    assert database["enabled"] == True