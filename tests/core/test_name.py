from JarvisEngine.core import name

def test_SEP():
    assert name.SEP == "."

def test_clean():
    assert name.clean("a.b.c") == "a.b.c"
    assert name.clean("d.e.") == "d.e"
    assert name.clean(".f.") == "f"
    assert name.clean(".g.h") == "g.h"