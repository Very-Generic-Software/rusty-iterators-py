from __future__ import annotations

from itertools import cycle
from typing import TYPE_CHECKING

import more_itertools as mi

from rusty_iterators import LIter

from .manager import BenchmarkManager

if TYPE_CHECKING:
    from collections.abc import Iterable


@BenchmarkManager.register(arg=list(range(1_000_000)))
def benchmark_rusty_iterators_sequence_wrapper(arg: Iterable[int]) -> None:
    _ = LIter.from_seq(arg).collect()  # type: ignore[arg-type]


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_map(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).map(lambda x: x * 2).collect()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_stdlib_map(arg: Iterable[int]) -> None:
    _ = list(map(lambda x: x * 2, iter(arg)))


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_filter(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).filter(lambda x: x % 2 == 0).collect()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_stdlib_filter(arg: Iterable[int]) -> None:
    _ = list(filter(lambda x: x % 2 == 0, iter(arg)))


@BenchmarkManager.register(arg=[1, 2, 3, 4, 5])
def benchmark_rusty_iterators_copy_cycle(arg: Iterable[int]) -> None:
    _ = LIter.from_items(*arg).cycle(use_cache=False).take(1_000_000).collect()


@BenchmarkManager.register(arg=[1, 2, 3, 4, 5])
def benchmark_rusty_iterators_cache_cycle(arg: Iterable[int]) -> None:
    _ = LIter.from_items(*arg).cycle(use_cache=True).take(1_000_000).collect()


@BenchmarkManager.register(arg=[1, 2, 3, 4, 5])
def benchmark_itertools_cycle(arg: Iterable[int]) -> None:
    it = cycle(arg)
    _ = [next(it) for _ in range(1_000_000)]


@BenchmarkManager.register(arg=[[i, i * 2] for i in range(1_000_000)])
def benchmark_rusty_iterators_flatten(arg: Iterable[list[int]]) -> None:
    _ = LIter.from_items(*arg).flatten().collect()


@BenchmarkManager.register(arg=[[i, i * 2] for i in range(1_000_000)])
def benchmark_more_itertools_flatten(arg: Iterable[list[int]]) -> None:
    _ = list(mi.flatten(arg))


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_count(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).count()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_stdlib_count(arg: Iterable[int]) -> None:
    _ = len(list(arg))


@BenchmarkManager.register(arg=[[i, i * 2] for i in range(1_000_000)])
def benchmark_more_itertools_unzip(arg: Iterable[list[int]]) -> None:
    left, right = mi.unzip(arg)
    list(left)
    list(right)


@BenchmarkManager.register(arg=[[i, i * 2] for i in range(1_000_000)])
def benchmark_rusty_iterators_unzip(arg: Iterable[list[int]]) -> None:
    _left, _right = LIter.from_items(*arg).unzip()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_more_itertools_filter_map(arg: Iterable[int]) -> None:
    _ = list(mi.filter_map(lambda x: x**2 if x % 2 == 0 else None, arg))


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_filter_map(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).filter(lambda x: x % 2 == 0).map(lambda x: x**2).collect()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_more_itertools_nth(arg: Iterable[int]) -> None:
    _ = mi.nth(arg, 999_999)


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_nth(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).nth(999_999)


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_more_itertools_take(arg: Iterable[int]) -> None:
    _ = list(mi.take(500_000, arg))


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_take(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).take(500_000).collect()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_rusty_iterators_unique(arg: Iterable[int]) -> None:
    _ = LIter.from_it(iter(arg)).unique().collect()


@BenchmarkManager.register(arg=range(1_000_000))
def benchmark_more_iterators_unique(arg: Iterable[int]) -> None:
    _ = list(mi.unique(arg))
