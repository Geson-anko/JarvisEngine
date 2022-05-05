import toml

def read_toml(file_path:str, mode:str="r", encoding:str="utf-8",**kwds) -> dict:
    """read toml file."""
    with open(file_path,mode,encoding=encoding,**kwds) as f:
        return toml.load(f)
