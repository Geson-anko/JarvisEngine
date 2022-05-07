SEP = "."

def clean(name:str) -> str:
    """clean name."""
    if name[0] == SEP:
        start = 1
    else:
        start = 0
    
    if name[-1] == SEP:
        end = -1
    else:
        end = len(name)

    return name[start:end]

def count_head_sep(name:str) -> int:
    """count number of head separator of name.
    Ex:
        "..a.b" -> 2
        "...c" -> 3
    """
    num = 0
    for s in name:
        if s != SEP:
            return num
        else:
            num += 1
    return num

def join(name:str, *others:str) -> str:
    """join names
    Ex: join("a.b.","c.d") -> "a.b.c.d"
    """
    name = clean(name)
    for n in others:
        n = clean(n)
        name = f"{name}{SEP}{n}"
    return name
