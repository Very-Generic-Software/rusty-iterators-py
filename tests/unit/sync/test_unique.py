from rusty_iterators import LIter


def test_unique_values() -> None:
    it = LIter.from_items(1, 2, 1, 3, 4, 2, 5, 1, 2)

    assert it.unique().collect() == [1, 2, 3, 4, 5]


def test_unique_copy() -> None:
    it = LIter.from_items(1, 2, 1, 3, 4, 2, 5, 1, 2).unique()
    cp = it.copy()

    it.next()

    assert it.collect() == [2, 3, 4, 5]
    assert cp.collect() == [1, 2, 3, 4, 5]


def test_unique_empty_iterator() -> None:
    assert LIter.from_items().unique().collect() == []
