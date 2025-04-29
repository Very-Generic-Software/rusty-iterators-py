from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from ._folders import FolderInterface
    from ._reducers import ReducerInterface


class ConsumerInterface[T, R](ABC):
    __slots__ = ()

    @abstractmethod
    def as_folder(self) -> FolderInterface[T, R]:
        raise NotImplementedError

    @abstractmethod
    def split(self, n: int) -> tuple[Self, Self, ReducerInterface[R]]:
        raise NotImplementedError
