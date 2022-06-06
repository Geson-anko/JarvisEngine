import collections.abc
from typing import Mapping

import json5
import toml
from attr_dict import AttrDict


def read_toml(file_path: str, mode: str = "r", encoding: str = "utf-8", **kwds) -> dict:
    """read toml file."""
    with open(file_path, mode, encoding=encoding, **kwds) as f:
        return toml.load(f)


def read_json(file_path: str, mode: str = "r", encoding: str = "utf-8", **kwds) -> dict:
    """read json and json5 files."""
    with open(file_path, mode, encoding=encoding, **kwds) as f:
        return json5.load(f)


def dict2attr(d: dict) -> AttrDict:
    """converts dict to AttrDict."""
    return AttrDict(d)


def deep_update(d: dict, u: Mapping) -> dict:
    """Deep update nested dict"""
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping) and v:
            d[k] = deep_update(d.get(k, dict()), v)
        else:
            d[k] = v

    return d
