SEP = "."

def clean(name:str) -> str:
    """clean name.
    Erase all SEP's at the head and tail of name.
    Ex:
        "..a.b.c.." -> "a.b.c"
        ".d.e" -> "d.e"
    """
    if name[0] == SEP:
        start = count_head_sep(name)
    else:
        start = 0
    
    if name[-1] == SEP:
        end = -count_head_sep(name[::-1])
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

def join_relatively(name:str, another:str) -> str:
    """Join another to name.
    Ex:
        join_relatively("a.b.c","..d.e") -> "a.b.d.e"
        join_relatively("a.", "...d.e.f") -> "d.e.f"
    """
    name = clean(name)
    n_sep = count_head_sep(another) - 1
    if n_sep > 0:
        splited = name.split(SEP)[:-n_sep]
        name = SEP.join(splited)
    another = clean(another)
    if name == "":
        return another
    else:
        return f"{name}{SEP}{another}"

def join(name:str, *others:str) -> str:
    """join names. Supported relative join.
    Ex: 
        join("a.b.","c.d") -> "a.b.c.d"
        join("a.b.c","..d.e","...e.c") -> "a.b.e.c"
    """
    name = clean(name)
    for n in others:
        name = join_relatively(name, n)
    return name
