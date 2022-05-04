from JarvisEngine.core import name

def test_SEP():
    assert name.SEP == "."

def test_clean():
    assert name.clean("a.b.c") == "a.b.c"
    assert name.clean("d.e.") == "d.e"
    assert name.clean(".f.") == "f"
    assert name.clean(".g.h") == "g.h"

def test_join():
    assert name.join("a","b") == "a.b"
    assert name.join("a.b.c") == "a.b.c"
    assert name.join(".a.b.","c.",".d") == "a.b.c.d"
    assert name.join("a","b","c","d") == "a.b.c.d"
    assert name.join(".a.b.c.d") == "a.b.c.d"