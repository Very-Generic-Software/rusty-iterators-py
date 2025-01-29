from __future__ import annotations

from collections.abc import Callable
from typing import Iterator, Self, Sequence, final, override

type FilterCallable[T] = Callable[[T], bool]
type MapCallable[T, R] = Callable[[T], R]

class IterInterface[T]:
    def __iter__(self) -> Self: ...
    def __next__(self) -> T: ...
    def collect(self) -> list[T]: ...
    def filter(self, func: FilterCallable[T]) -> Filter[T]: ...
    def map[R](self, func: MapCallable[T, R]) -> Map[T, R]: ...
    def next(self) -> T: ...

@final
class Filter[T](IterInterface[T]):
    def __init__(self, other: IterInterface[T], func: FilterCallable[T]) -> None: ...
    @override
    def next(self) -> T: ...

@final
class Map[T, R](IterInterface[R]):
    def __init__(self, other: IterInterface[T], func: MapCallable[T, R]) -> None: ...
    @override
    def next(self) -> R: ...

@final
class SeqWrapper[T](IterInterface[T]):
    def __init__(self, s: Sequence[T]) -> None: ...
    def copy(self) -> bool: ...

@final
class IterWrapper[T](IterInterface[T]):
    def __init__(self, it: Iterator[T]) -> None: ...
    def copy(self) -> bool: ...
