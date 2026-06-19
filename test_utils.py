import pytest
from utils import clamp, merge_sorted, parse_pair, unique_sorted

# --- Тесты для clamp (включая убийц мутантов) ---
def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
    # Убивают мутантов, меняющих < на <=
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10
    # Убивает мутантов, ломающих логику lo/hi
    assert clamp(5, 5, 5) == 5

# --- Тесты для merge_sorted (включая убийц мутантов) ---
def test_merge_sorted():
    assert merge_sorted([1, 3], [2, 4]) == [1, 2, 3, 4]
    # Убивает мутанта с заменой <= на <
    assert merge_sorted([1, 2, 2], [2, 3]) == [1, 2, 2, 2, 3]
    # Пустые массивы
    assert merge_sorted([], [1, 2]) == [1, 2]
    assert merge_sorted([1, 2], []) == [1, 2]
    assert merge_sorted([], []) == []

# --- Тесты для parse_pair ---
def test_parse_pair():
    assert parse_pair("10:20") == (10, 20)
    with pytest.raises(ValueError):
        parse_pair("hello")
    with pytest.raises(ValueError):
        parse_pair("1:2:3")
    with pytest.raises(ValueError):
        parse_pair("a:b")

# --- Тест для unique_sorted (Ловит баг!) ---
def test_unique_sorted_bug():
    # Из-за сдвига индекса в коде, три одинаковых числа подряд вызовут ошибку
    assert unique_sorted([1, 2, 2, 2, 3]) == [1, 2, 3]