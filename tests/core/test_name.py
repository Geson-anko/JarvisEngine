from JarvisEngine.core import name


def test_SEP():
    assert name.SEP == "."


def test_clean():
    assert name.clean("a.b.c") == "a.b.c"
    assert name.clean("d.e.") == "d.e"
    assert name.clean(".f.") == "f"
    assert name.clean(".g.h") == "g.h"

    assert name.clean("..a.b.c..") == "a.b.c"
    assert name.clean("..d.e") == "d.e"
    assert name.clean("f....") == "f"


def test_join():
    assert name.join("a", "b") == "a.b"
    assert name.join("a.b.c") == "a.b.c"
    assert name.join(".a.b.", "c.", ".d") == "a.b.c.d"
    assert name.join("a", "b", "c", "d") == "a.b.c.d"
    assert name.join(".a.b.c.d") == "a.b.c.d"
    assert name.join("a.b.c", "..d.e", "...e.c") == "a.b.e.c"


def test_count_head_sep():
    assert name.count_head_sep("..a.b.") == 2
    assert name.count_head_sep("") == 0
    assert name.count_head_sep(".....") == 5
    assert name.count_head_sep("asf....") == 0
    assert name.count_head_sep("..v..s..a.sd") == 2


def test_join_relatively():
    assert name.join_relatively("a.b.c", "..d.e") == "a.b.d.e"
    assert name.join_relatively("a.", "...d.e.f") == "d.e.f"
    assert name.join_relatively("a.b.c", ".d.e") == "a.b.c.d.e"
    assert name.join_relatively("a", "b") == "a.b"
