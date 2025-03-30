import pytest

from rusty_iterators import LIter


def test_next_returns_next_element() -> None:
    it = LIter.from_items(1, 2, 3)

    assert it.next() == 1
    assert it.next() == 2
    assert it.next() == 3


def test_next_on_empty_iterator() -> None:
    it = LIter.from_items()

    with pytest.raises(StopIteration):
        it.next()


def test_collect_returns_original_items() -> None:
    assert LIter.from_items(1, 2, 3).collect() == [1, 2, 3]


def test_collect_into() -> None:
    assert LIter.from_items(1, 2, 3).collect_into(tuple) == (1, 2, 3)
    assert LIter.from_items(1, 2, 3).collect_into(list) == [1, 2, 3]
    assert LIter.from_items(1, 2, 3).collect_into(set) == {1, 2, 3}
    assert LIter.from_items(1, 2, 3).collect_into(frozenset) == {1, 2, 3}


def test_unzip_tuple_iterator() -> None:
    left, right = LIter.from_items((1, "a"), (2, "b"), (3, "c")).unzip()

    assert left == [1, 2, 3]
    assert right == ["a", "b", "c"]


def test_unzip_list_iterator() -> None:
    left, right = LIter.from_items([1, 2], [3, 4], [5, 6]).unzip()

    assert left == [1, 3, 5]
    assert right == [2, 4, 6]


def test_sum_returns_summed_items() -> None:
    assert LIter.from_items(1, 2, 3).sum() == 6


def test_sum_empty_iterator() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().sum()


def test_sum_iterator_using_fold() -> None:
    assert LIter.from_items(1, 2, 3, 4).fold(0, lambda acc, x: acc + x) == 10


def test_build_accumulated_string_with_fold() -> None:
    assert LIter.from_items(1, 2, 3, 4).fold("0", lambda acc, x: f"({acc} + {x})") == "((((0 + 1) + 2) + 3) + 4)"


def test_sum_iterator_using_reduce() -> None:
    assert LIter.from_items(1, 2, 3, 4).reduce(lambda acc, x: acc + x) == 10


def test_nth_returns_correct_element() -> None:
    assert LIter.from_items(1, 2, 3).nth(2) == 3


def test_nth_throws_when_size_exceeded() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items(1, 2, 3).nth(3)


def test_last_returns_last_item() -> None:
    assert LIter.from_items(1, 2, 3).last() == 3


def test_last_on_empty_iterator() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().last()


def test_for_each() -> None:
    storage = []
    LIter.from_items(1, 2, 3).for_each(lambda x: storage.append(x))

    assert storage == [1, 2, 3]


@pytest.mark.parametrize("arg", ([1, 2, 3], []))
def test_count_iterator_elements(arg: list[int]) -> None:
    assert LIter.from_seq(arg).count() == len(arg)


def test_max_returns_the_max_item() -> None:
    assert LIter.from_items(1, 2, 3).max() == 3


def test_max_called_on_empty_iterator() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().max()


def test_min_returns_the_min_item() -> None:
    assert LIter.from_items(1, 2, 3).min() == 1


def test_min_called_on_empty_iterator() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().min()


def test_product_returns_the_product_of_items() -> None:
    assert LIter.from_items(1, 2, 3).product() == 6


def test_product_called_on_empty_iterator() -> None:
    with pytest.raises(StopIteration):
        LIter.from_items().product()
