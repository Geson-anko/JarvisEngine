import toml
import json5

def read_toml(file_path:str, mode:str="r", encoding:str="utf-8",**kwds) -> dict:
    """read toml file."""
    with open(file_path,mode,encoding=encoding,**kwds) as f:
        return toml.load(f)

def read_json(file_path:str, mode:str="r", encoding:str="utf-8",**kwds) -> dict:
    """read json and json5 files."""
    with open(file_path,mode, encoding=encoding,**kwds) as f:
        return json5.load(f)
        