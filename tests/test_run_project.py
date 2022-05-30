from JarvisEngine.run_project import create_shutdown

# prepare
from JarvisEngine.constants import SHUTDOWN_NAME
from JarvisEngine.core.value_sharing import (
    ReadOnlyValue, FolderDict_withLock
)
from multiprocessing.sharedctypes import Synchronized

def test_create_shutdown():
    fdwl = FolderDict_withLock()
    shutdown = create_shutdown(fdwl)
    shutdown_readonly = fdwl[SHUTDOWN_NAME]
    
    assert isinstance(shutdown, Synchronized)
    assert isinstance(shutdown_readonly, ReadOnlyValue)
    assert shutdown.value == False
    assert shutdown_readonly.value == False
