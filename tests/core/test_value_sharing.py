import ctypes
import multiprocessing as mp
import threading
from typing import *

from JarvisEngine.core import value_sharing
from JarvisEngine.core.value_sharing import ReadOnly, ReadOnlyArray, ReadOnlyError, ReadOnlyString, ReadOnlyValue


def assert_modify_value(obj: Union[ReadOnlyValue, ReadOnlyString]):
    try:
        obj.value = None
        raise AssertionError
    except ReadOnlyError:
        pass


def assert_modify_array(obj: Union[ReadOnlyArray, ReadOnlyString]):
    try:
        obj[0] = None
        raise AssertionError
    except ReadOnlyError:
        try:
            obj[:] = None
        except ReadOnlyError:
            pass


def assert_modify_string(obj: ReadOnlyString):
    try:
        obj.raw = None
        raise AssertionError
    except ReadOnlyError:
        assert_modify_value(obj)
        assert_modify_array(obj)


def test_ReadOnly():
    value = mp.Value(ctypes.c_int, 0)
    ro = ReadOnly(value)

    assert ro._obj == value
    assert ro._lock == value._lock
    assert ro.get_lock() == value.get_lock()
    assert ro.get_obj() == value.get_obj()
    assert ro.acquire == value.acquire
    assert ro.release == value.release
    assert repr(ro) == f"ReadOnly{repr(value)}"
    assert ro.get_type() == type(value)


def test_ReadOnlyValue():
    v0 = mp.Value(ctypes.c_bool)
    v1 = mp.Value(ctypes.c_float)
    ro0 = ReadOnlyValue(v0)
    ro1 = ReadOnlyValue(v1)
    assert issubclass(ReadOnlyValue, ReadOnly)
    assert ro0.value == v0.value
    assert ro1.value == v1.value
    assert_modify_value(ro0)
    assert_modify_value(ro1)


def test_ReadOnlyArray():
    a0 = mp.Array(ctypes.c_longdouble, 10)
    a1 = mp.Array(ctypes.c_bool, 3)
    roa0 = ReadOnlyArray(a0)
    roa1 = ReadOnlyArray(a1)

    assert len(roa0) == 10
    assert len(roa1) == 3
    assert roa0[0] == a0[0]
    assert roa1[2] == a1[2]
    assert roa0[:4] == a0[:4]
    assert roa1[0:10] == a1[0:10]

    assert_modify_array(roa0)
    assert_modify_array(roa1)


def test_ReadOnlyString():
    s0 = mp.Array(ctypes.c_char, 10)
    ros0 = ReadOnlyString(s0)

    assert len(ros0) == 10
    assert ros0[1] == s0[1]
    assert ros0[3:10] == s0[3:10]

    assert_modify_string(ros0)


def test_make_readonly():

    v = mp.Value("i")
    a = mp.Array(ctypes.c_uint8, 3)
    s = mp.Array(ctypes.c_char, 10)

    rov = value_sharing.make_readonly(v)
    roa = value_sharing.make_readonly(a)
    ros = value_sharing.make_readonly(s)

    assert isinstance(rov, ReadOnlyValue)
    assert isinstance(roa, ReadOnlyArray)
    assert isinstance(ros, ReadOnlyString)

    try:
        value_sharing.make_readonly(None)
        raise AssertionError
    except ValueError:
        pass


def test_FolderDict_withLock():
    fdwl = value_sharing.FolderDict_withLock(sep=".")
    rlock_type = type(threading.RLock())
    assert isinstance(fdwl._lock, rlock_type)
    assert fdwl._lock == fdwl.get_lock()

    lock = threading.RLock()
    fdwl = value_sharing.FolderDict_withLock(sep=".", lock=lock)
    assert fdwl.get_lock() == lock

    # Not implemented locking test because I don't know how to test it.
    fdwl["a.b.c"] = 1
    fdwl["a.b.c"]
