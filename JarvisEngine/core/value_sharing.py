import threading
from multiprocessing.sharedctypes import Synchronized, SynchronizedArray, SynchronizedBase, SynchronizedString
from typing import *

from folder_dict import FolderDict

from .name import SEP


class ReadOnlyError(Exception):
    pass


class ReadOnly(object):
    """Read Only Synchronized object.
    Wrapps `multiprocessing.sharedctypes.SynchronizedBase`.
    """

    def __init__(self, value: SynchronizedBase) -> None:
        self._obj = value
        self._lock = value.get_lock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    def __reduce__(self):
        return self._obj.__reduce__()

    def get_obj(self):
        return self._obj.get_obj()

    def get_lock(self):
        return self._obj.get_lock()

    def __repr__(self) -> str:
        return f"ReadOnly{repr(self._obj)}"

    def get_type(self):
        return type(self._obj)


class ReadOnlyValue(ReadOnly):
    """Wrapps `multiprocessing.sharedctypes.Synchronized`"""

    _obj: Synchronized

    @property
    def value(self):
        return self._obj.value

    @value.setter
    def value(self,*args):
        raise ReadOnlyError


class ReadOnlyArray(ReadOnly):
    """Wrapps `multiprocessing.sharedctypes.SynchronizedArray`"""

    _obj: SynchronizedArray

    def __len__(self):
        return len(self._obj)

    def __getitem__(self, i: Any):
        return self._obj[i]

    def __getslice__(self, start: int, stop: int):
        return self._obj.__getslice__(start, stop)

    def __setitem__(self,*args):
        raise ReadOnlyError

    def __setslice__(self,*args):
        raise ReadOnlyError


class ReadOnlyString(ReadOnlyArray):
    """Wrapps `multiprocessing.sharedctypes.SynchronizedString`"""

    _obj: SynchronizedString

    @property
    def value(self):
        return self._obj.value

    @value.setter
    def value(self,*args):
        raise ReadOnlyError

    @property
    def raw(self):
        return self.raw

    @raw.setter
    def raw(self,*args):
        raise ReadOnlyError


def make_readonly(
    value: Union[Synchronized, SynchronizedArray, SynchronizedString]
) -> Union[ReadOnlyValue, ReadOnlyArray, ReadOnlyString]:
    """Make synchronized objects readonly."""

    if isinstance(value, Synchronized):
        return ReadOnlyValue(value)
    elif isinstance(value, SynchronizedString):  # check before array.
        return ReadOnlyString(value)
    elif isinstance(value, SynchronizedArray):
        return ReadOnlyArray(value)
    else:
        raise ValueError(
            f"Unknown type {type(value)}. " "Please Synchronized, SynchronizedArray or SynchronizedString."
        )


class FolderDict_withLock(FolderDict):
    """
    Protects FolderDict with Lock to prevent multiple threads
    from reading and writing at the same time
    """

    def __init__(
        self,
        data=None,
        deep_copy: bool = False,
        *,
        sep: str = SEP,
        lock=None,
    ) -> None:
        super().__init__(data, deep_copy, sep=sep)

        if lock is None:
            self._lock = threading.RLock()
        else:
            self._lock = lock

    def get_lock(self) -> Union[threading.RLock, Any]:
        """returns lock object."""
        return self._lock

    def __getitem__(self, path: Union[str, Iterable[str]]) -> Union[Any, List[str]]:
        with self._lock:
            return super().__getitem__(path)

    def __setitem__(self, path: Union[str, Iterable[str]], value: Union[Any, Iterable[Any]]) -> None:
        with self._lock:
            return super().__setitem__(path, value)
