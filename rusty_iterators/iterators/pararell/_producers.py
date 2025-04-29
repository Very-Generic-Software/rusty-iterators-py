from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from rusty_iterators.iterators._sync import IterInterface


class ProducerInterface[T](ABC):
    __slots__ = ()

    @abstractmethod
    def as_iter(self) -> IterInterface[T]:
        raise NotImplementedError

    @abstractmethod
    def split(self, n: int) -> tuple[Self, Self]:
        raise NotImplementedError
