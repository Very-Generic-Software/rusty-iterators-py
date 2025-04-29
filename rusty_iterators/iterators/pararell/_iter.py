from __future__ import annotations

from abc import ABC, abstractmethod


class PararellIterInterface[T](ABC):
    __slots__ = ()

    @abstractmethod
    def size_hint(self) -> int:
        raise NotImplementedError
