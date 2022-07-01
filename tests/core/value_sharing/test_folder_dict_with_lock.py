import threading

from JarvisEngine.core.value_sharing import folder_dict_with_lock


def test_FolderDictWithLock():
    fdwl = folder_dict_with_lock.FolderDictWithLock(sep=".")
    rlock_type = type(threading.RLock())
    assert isinstance(fdwl._lock, rlock_type)
    assert fdwl._lock == fdwl.get_lock()

    lock = threading.RLock()
    fdwl = folder_dict_with_lock.FolderDictWithLock(sep=".", lock=lock)
    assert fdwl.get_lock() == lock

    # Not implemented locking test because I don't know how to test it.
    fdwl["a.b.c"] = 1
    fdwl["a.b.c"]
