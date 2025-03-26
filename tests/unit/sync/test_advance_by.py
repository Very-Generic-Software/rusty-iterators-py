import pytest

from rusty_iterators import LIter


def test_advance_by() -> None:
    it = LIter.from_items(1, 2, 3, 4)
    it.advance_by(2)

    assert it.collect() == [3, 4]


def test_advance_by_negative_idx() -> None:
    with pytest.raises(ValueError):
        LIter.from_items().advance_by(-1)
