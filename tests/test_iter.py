from typing import Iterator

import pytest

from rusty_iterators import Iter


class TestIteratorConstructors:
    def test_from_items_builds_a_generator(self) -> None:
        it = Iter.from_items(1, 2, 3)

        assert [x for x in it.gen] == [1, 2, 3]

    def test_from_iterable_builds_a_generator(self) -> None:
        arr = [1, 2, 3]
        it = Iter.from_iterable(arr)

        assert [x for x in it.gen] == arr


class TestIteratorNext:
    def test_next_advances_an_iterator(self, gen: Iterator[int]) -> None:
        it = Iter(gen)

        result = it.next()
        assert result.exists and result.value == 1

        result = it.next()
        assert result.exists and result.value == 2

    def test_next_returns_none_when_iterator_is_depleted(self, empty_gen: Iterator[int]) -> None:
        it = Iter(empty_gen)

        assert it.next().exists is False


class TestIteratorCollect:
    def test_collect_iterator_to_list(self, gen: Iterator[int]) -> None:
        result = Iter(gen).collect()

        assert result == [1, 2, 3, 4]

    def test_iterator_cannot_be_collected_multiple_times(self, gen: Iterator[int]) -> None:
        it = Iter(gen)

        assert it.collect() == [1, 2, 3, 4]
        assert it.collect() == []

    def test_iterator_allows_user_to_collect_null_values(self) -> None:
        # In the early version of the interface, the `.next()` method
        # used `None` as an indication that iterator is depleted. This
        # introduced confusion regarding the existance of `None` values
        # in the iterator itself, so it was redesigned. This test is
        # a sanity check.
        gen = (x for x in [None, None, None])
        result = Iter(gen).collect()

        assert result == [None, None, None]


class TestIteratorCount:
    def test_count_returns_amount_of_elements(self, gen: Iterator[int]) -> None:
        result = Iter(gen).count()

        assert result == 4

    def test_count_on_empty_iterator(self, empty_gen: Iterator[int]) -> None:
        result = Iter(empty_gen).count()

        assert result == 0


class TestIteratorLast:
    def test_last_returns_last_item(self, gen: Iterator[int]) -> None:
        result = Iter(gen).last()

        assert result.exists and result.value == 4

    def test_last_returns_no_value_when_empty(self, empty_gen: Iterator[int]) -> None:
        result = Iter(empty_gen).last()

        assert result.exists is False


class TestIteratorCopy:
    def test_copied_iterator_depletes_separately(self, gen: Iterator[int]) -> None:
        it_orig = Iter(gen)
        it_copy = it_orig.copy()

        assert it_orig.collect() == [1, 2, 3, 4]
        assert it_copy.collect() == [1, 2, 3, 4]


class TestIteratorAdvanceBy:
    def test_advance_by(self, gen: Iterator[int]) -> None:
        result = Iter(gen).advance_by(2).collect()

        assert result == [3, 4]

    def test_advance_by_depleted_iterator(self, gen: Iterator[int]) -> None:
        result = Iter(gen).advance_by(5).collect()

        assert result == []

    def test_advance_by_negative_index(self, gen: Iterator[int]) -> None:
        with pytest.raises(ValueError):
            Iter(gen).advance_by(-1)


class TestIteratorNth:
    def test_first_element(self, gen: Iterator[int]) -> None:
        result = Iter(gen).nth(0)

        assert result.exists and result.value == 1

    def test_nth_element(self, gen: Iterator[int]) -> None:
        result = Iter(gen).nth(3)

        assert result.exists and result.value == 4

    def test_non_existant_element(self, gen: Iterator[int]) -> None:
        result = Iter(gen).nth(4)

        assert result.exists is False

    def test_negative_index(self, gen: Iterator[int]) -> None:
        with pytest.raises(ValueError):
            Iter(gen).nth(-1)
