from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self


class FolderInterface[T, R](ABC):
    __slots__ = ()

    @abstractmethod
    def consume(self, item: T) -> Self:
        raise NotImplementedError

    @abstractmethod
    def complete(self) -> R:
        raise NotImplementedError
