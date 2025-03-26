from rusty_iterators import LIter


def test_next_skip_n_elements() -> None:
    it = LIter.from_items(1, 2, 3).skip(2)

    assert it.next() == 3


def test_copy_before_skip() -> None:
    it = LIter.from_items(1, 2, 3).skip(2)
    cp = it.copy()

    assert it.next() == 3
    assert cp.next() == 3


def test_copy_after_skip() -> None:
    it = LIter.from_items(1, 2, 3).skip(1)
    it.next()

    cp = it.copy()

    assert it.next() == 3
    assert cp.next() == 3
