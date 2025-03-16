from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Optional, TypeAlias, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    T = TypeVar("T")

    BenchmarkCallable: TypeAlias = Callable[[Iterable[T]], None]
    BenchmarkStorage: TypeAlias = dict[str, tuple[BenchmarkCallable[T], Iterable[T]]]
    BenchmarkItem: TypeAlias = tuple[str, tuple[BenchmarkCallable[T], Iterable[T]]]


class BenchmarkManager:
    _storage: ClassVar[BenchmarkStorage[Any]] = {}

    @classmethod
    def register(cls, *, arg: Iterable[T]) -> Callable[[BenchmarkCallable[T]], BenchmarkCallable[T]]:
        def inner(benchmark: BenchmarkCallable[T]) -> BenchmarkCallable[T]:
            cls._storage[benchmark.__name__] = (benchmark, arg)
            return benchmark

        return inner

    @classmethod
    def get_benchmark_names(cls) -> list[str]:
        return list(cls._storage.keys())

    @classmethod
    def get_benchmarks(cls, names: Optional[list[str]] = None) -> list[BenchmarkItem[Any]]:
        if names:
            return [(name, cls._storage[name]) for name in names]

        return list(cls._storage.items())
