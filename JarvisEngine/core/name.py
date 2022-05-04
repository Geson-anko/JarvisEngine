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
    