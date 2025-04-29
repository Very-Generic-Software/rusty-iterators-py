from __future__ import annotations

from abc import ABC, abstractmethod


class ReducerInterface[R](ABC):
    __slots__ = ()

    @abstractmethod
    def reduce(self, left: R, right: R) -> R:
        raise NotImplementedError
