import pytest
from utils import clamp, merge_sorted, parse_pair, unique_sorted


def test_clamp_inside():
    assert clamp(5, 0, 10) == 5

def test_clamp_below():
    assert clamp(-5, 0, 10) == 0

def test_clamp_above():
    assert clamp(15, 0, 10) == 10

def test_clamp_on_boundary():
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10

def test_clamp_equal_bounds():
    assert clamp(5, 5, 5) == 5


def test_merge_sorted_normal():
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

def test_merge_sorted_empty():
    assert merge_sorted([], [1, 2]) == [1, 2]
    assert merge_sorted([1, 2], []) == [1, 2]
    assert merge_sorted([], []) == []

def test_merge_sorted_duplicates():
    assert merge_sorted([1, 2, 2], [2, 3]) == [1, 2, 2, 2, 3]

# --- Тесты для parse_pair ---
def test_parse_pair_valid():
    assert parse_pair("10:20") == (10, 20)

def test_parse_pair_no_separator():
    with pytest.raises(ValueError):
        parse_pair("hello")

def test_parse_pair_too_many_separators():
    with pytest.raises(ValueError):
        parse_pair("1:2:3")

def test_parse_pair_not_integers():
    with pytest.raises(ValueError):
        parse_pair("a:b")


def test_unique_sorted_bug():

    assert unique_sorted([1, 2, 2, 2, 3]) == [1, 2, 3]