import pytest

from rusty_iterators import RustyIter


def test_invalid_iterator_structure() -> None:
    # This is not allowed and will crash, so `type: ignore` is needed.
    it = RustyIter.from_items(1, 2, 3, [3]).flatten()  # type: ignore[misc, var-annotated]

    with pytest.raises(TypeError):
        it.collect()


def test_single_flatten() -> None:
    it = RustyIter.from_items([1, 2, 3], [4, 5, 6]).flatten()

    assert it.collect() == [1, 2, 3, 4, 5, 6]


def test_double_flatten() -> None:
    it = RustyIter.from_items([[1], [2], [3]], [[4], [5], [6]]).flatten().flatten()

    assert it.collect() == [1, 2, 3, 4, 5, 6]
