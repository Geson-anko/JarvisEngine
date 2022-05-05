from JarvisEngine.core import config_tools

def test_read_toml():
    conf = config_tools.read_toml("tests/core/test_config.toml")
    assert conf["title"] == "TOML Example"
    
    database = conf["database"]
    assert database["server"] == "192.168.1.1"
    assert database["ports"] == [ 8000, 8001, 8002 ]
    assert database["connection_max"] == 5000
    assert database["enabled"] == True

def test_read_json():
    conf = config_tools.read_json("tests/core/test_config.json5")
    assert conf["name"] == "geson"
    assert conf["age"] == 18
    assert conf["sex"]["real"] == "male"
    assert conf["sex"]["virtual"] == "female"
    assert conf["student"] == True

def test_dict2attr():
    d = {
        "name": "geson",
        "age": 18,
        "sex": {
            "real": "male",
            "virtual": "female"
        },
        "student": True,
    }
    conf = config_tools.dict2attr(d)
    assert conf.name == "geson"
    assert conf.age == 18
    assert conf.sex.real == "male"
    assert conf.sex.virtual == "female"
    assert conf.student== True