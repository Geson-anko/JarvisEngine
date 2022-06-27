import threading
from typing import *

from folder_dict import FolderDict

from ..name import SEP


class FolderDictWithLock(FolderDict):
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
