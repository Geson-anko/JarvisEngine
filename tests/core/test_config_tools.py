from typing import Dict, Union

from JarvisEngine.core import config_tools


def test_read_toml():
    conf = config_tools.read_toml("tests/core/test_config.toml")
    assert conf["title"] == "TOML Example"

    database = conf["database"]
    assert database["server"] == "192.168.1.1"
    assert database["ports"] == [8000, 8001, 8002]
    assert database["connection_max"] == 5000
    assert database["enabled"] is True


def test_read_json():
    conf = config_tools.read_json("tests/core/test_config.json5")
    assert conf["name"] == "geson"
    assert conf["age"] == 18
    assert conf["sex"]["real"] == "male"
    assert conf["sex"]["virtual"] == "female"
    assert conf["student"] is True


def test_dict2attr():
    d = {
        "name": "geson",
        "age": 18,
        "sex": {"real": "male", "virtual": "female"},
        "student": True,
    }
    conf = config_tools.dict2attr(d)
    assert conf.name == "geson"
    assert conf.age == 18
    assert conf.sex.real == "male"
    assert conf.sex.virtual == "female"
    assert conf.student is True


def test_deep_update():
    source: Dict[str, Union[int, str, dict]] = {"hello1": 1}
    overrides: Dict[str, Union[int, str, dict]] = {"hello2": 2}
    config_tools.deep_update(source, overrides)
    assert source == {"hello1": 1, "hello2": 2}

    source = {"hello": "to_override"}
    overrides = {"hello": "over"}
    config_tools.deep_update(source, overrides)
    assert source == {"hello": "over"}

    source = {"hello": {"value": "to_override", "no_change": 1}}
    overrides = {"hello": {"value": "over"}}
    config_tools.deep_update(source, overrides)
    assert source == {"hello": {"value": "over", "no_change": 1}}

    source = {"hello": {"value": "to_override", "no_change": 1}}
    overrides = {"hello": {"value": {}}}
    config_tools.deep_update(source, overrides)
    assert source == {"hello": {"value": {}, "no_change": 1}}

    source = {"hello": {"value": {}, "no_change": 1}}
    overrides = {"hello": {"value": 2}}
    config_tools.deep_update(source, overrides)
    assert source == {"hello": {"value": 2, "no_change": 1}}
