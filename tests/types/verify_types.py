from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    from typing_extensions import Never, assert_type
else:
    from typing import Never, assert_type

from typing import TYPE_CHECKING, Any

from rusty_iterators import LIter

if TYPE_CHECKING:
    from collections.abc import Iterator

    from rusty_iterators.core.interface import (
        CacheCycle,
        CacheMovingWindow,
        Chain,
        CopyCycle,
        CopyMovingWindow,
        Enumerate,
        Filter,
        Flatten,
        Inspect,
        Map,
        Peekable,
        Skip,
        StepBy,
        Take,
        Unique,
        Zip,
    )
    from rusty_iterators.core.wrappers import IterWrapper, SeqWrapper


def verify_all_collect_into_variants() -> None:
    class CustomBuilder:
        def __init__(self, val: Iterator[int]) -> None:
            pass

    it = LIter.from_items(1, 2, 3)

    assert_type(it.collect_into(tuple), tuple[int, ...])
    assert_type(it.collect_into(list), list[int])
    assert_type(it.collect_into(set), set[int])
    assert_type(it.collect_into(frozenset), frozenset[int])
    assert_type(it.collect_into(CustomBuilder), CustomBuilder)


def verify_empty_items_iterator_type() -> None:
    it = LIter.from_items()

    assert_type(it, SeqWrapper[Any])
    assert_type(it.next(), Any)
    assert_type(it.collect(), list[Any])
    assert_type(it.sum(), Any)


def verify_items_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3)

    assert_type(it, SeqWrapper[int])
    assert_type(it.advance_by(2), None)
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])
    assert_type(it.sum(), int)
    assert_type(it.fold("", lambda acc, item: acc + str(item)), str)
    assert_type(it.reduce(lambda acc, x: acc + x), int)
    assert_type(it.nth(5), int)
    assert_type(it.last(), int)
    assert_type(it.for_each(lambda x: None), None)
    assert_type(it.count(), int)


def verify_empty_sequence_iterator_type() -> None:
    it = LIter.from_seq([])

    assert_type(it, SeqWrapper[Any])
    assert_type(it.next(), Any)
    assert_type(it.collect(), list[Any])
    assert_type(it.sum(), Any)


def verify_sequence_iterator_type() -> None:
    it = LIter.from_seq([1, 2, 3])

    assert_type(it, SeqWrapper[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])
    assert_type(it.sum(), int)


def verify_string_sequence_iterator_type() -> None:
    it = LIter.from_seq("abc")

    assert_type(it, SeqWrapper[str])
    assert_type(it.next(), str)
    assert_type(it.collect(), list[str])
    assert_type(it.sum(), str)


def verify_iterator_type() -> None:
    it = LIter.from_it(iter(range(10)))

    assert_type(it, IterWrapper[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_map_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).map(lambda x: str(x))

    assert_type(it, Map[str])
    assert_type(it.next(), str)
    assert_type(it.collect(), list[str])


def verify_filter_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).filter(lambda x: x % 2 == 0)

    assert_type(it, Filter[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_cycle_copy_iterator_type() -> None:
    it = LIter.from_items(1, 2).cycle(use_cache=False)

    assert_type(it, CopyCycle[int])
    assert_type(it.next(), int)


def verify_cycle_cache_iterator_type() -> None:
    it = LIter.from_items(1, 2).cycle(use_cache=True)

    assert_type(it, CacheCycle[int])
    assert_type(it.next(), int)


def verify_zip_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).zip(LIter.from_items("a", "b"))

    assert_type(it, Zip[int, str])
    assert_type(it.next(), tuple[int, str])
    assert_type(it.collect(), list[tuple[int, str]])


def verify_unzip_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).zip(LIter.from_items("a", "b"))

    assert_type(it.unzip(), tuple[list[int], list[str]])

    other_it = LIter.from_items([1, 2], [3, 4], [5, 6])

    assert_type(other_it.unzip(), tuple[list[int], list[int]])

    unzippable = LIter.from_items(1, 2, 3)

    # Even a simple call to unzip on unzippable type returns a type error
    # but if someone would force it, then the `Never` type is returned.
    assert_type(unzippable.unzip(), tuple[list[Never], list[Never]])  # type:ignore[misc]


def verify_take_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).take(5)

    assert_type(it, Take[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_step_by_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).step_by(2)

    assert_type(it, StepBy[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_all_type() -> None:
    assert_type(LIter.from_items(1, 2, 3).all(), bool)
    assert_type(LIter.from_items(1, 2, 3).all(lambda x: x > 2), bool)


def verify_any_type() -> None:
    assert_type(LIter.from_items(1, 2, 3).any(), bool)
    assert_type(LIter.from_items(1, 2, 3).any(lambda x: x > 2), bool)


def verify_chain_type() -> None:
    it = LIter.from_seq("abc").chain(LIter.from_seq("def"))

    assert_type(it, Chain[str])
    assert_type(it.next(), str)


def verify_cache_moving_window_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).moving_window(2)

    assert_type(it, CacheMovingWindow[int])
    assert_type(it.next(), list[int])
    assert_type(it.collect(), list[list[int]])


def verify_copy_moving_window_iterator_type() -> None:
    it = LIter.from_items(1, 2, 3).moving_window(2, use_cache=False)

    assert_type(it, CopyMovingWindow[int])
    assert_type(it.next(), list[int])
    assert_type(it.collect(), list[list[int]])


def verify_enumerate_type() -> None:
    it = LIter.from_items("a", "b").enumerate()

    assert_type(it, Enumerate[str])
    assert_type(it.next(), tuple[int, str])
    assert_type(it.collect(), list[tuple[int, str]])


def verify_flatten_type() -> None:
    it = LIter.from_items([1, 2], [3, 4]).flatten()

    assert_type(it, Flatten[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_inspect_type() -> None:
    it = LIter.from_items(1, 2, 3, 4).filter(lambda x: x % 2 == 0).inspect()

    assert_type(it, Inspect[int])
    assert_type(it.next(), int)


def verify_unique_type() -> None:
    it = LIter.from_items(1, 2, 3).unique()

    assert_type(it, Unique[int])
    assert_type(it.next(), int)
    assert_type(it.collect(), list[int])


def verify_peekable_type() -> None:
    it = LIter.from_items(1, 2, 3).peekable()

    assert_type(it, Peekable[int])
    assert_type(it.next(), int)
    assert_type(it.peek(), int)


def verify_skip_type() -> None:
    it = LIter.from_items(1, 2, 3).skip(2)

    assert_type(it, Skip[int])
    assert_type(it.next(), int)
