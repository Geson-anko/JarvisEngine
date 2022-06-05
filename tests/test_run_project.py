from multiprocessing.sharedctypes import Synchronized

# prepare
from JarvisEngine.constants import SHUTDOWN_NAME
from JarvisEngine.core.value_sharing import FolderDict_withLock, ReadOnlyValue
from JarvisEngine.run_project import create_shutdown


def test_create_shutdown():
    fdwl = FolderDict_withLock()
    shutdown = create_shutdown(fdwl)
    shutdown_readonly = fdwl[SHUTDOWN_NAME]

    assert isinstance(shutdown, Synchronized)
    assert isinstance(shutdown_readonly, ReadOnlyValue)
    assert shutdown.value == False
    assert shutdown_readonly.value == False
