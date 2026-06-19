from hypothesis import given, assume
from hypothesis import strategies as st
from utils import clamp, merge_sorted
from hypothesis import settings, HealthCheck
@settings(suppress_health_check=[HealthCheck.filter_too_much])

# --- Свойства для clamp ---
@given(st.integers(), st.integers(), st.integers())
def test_clamp_in_bounds(x, lo, hi):
    assume(lo <= hi) # Проверяем только логичные диапазоны
    result = clamp(x, lo, hi)
    assert lo <= result <= hi

@given(st.integers(), st.integers(), st.integers())
def test_clamp_idempotence(x, lo, hi):
    assume(lo <= hi)
    once = clamp(x, lo, hi)
    twice = clamp(once, lo, hi)
    assert once == twice # Применение clamp дважды не меняет результат

@given(st.integers(), st.integers(), st.integers())
def test_clamp_no_op(x, lo, hi):
    assume(lo <= x <= hi)
    assert clamp(x, lo, hi) == x # Если число уже в диапазоне, оно не меняется

# --- Свойства для merge_sorted ---
sorted_lists = st.lists(st.integers()).map(sorted)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_is_sorted(a, b):
    result = merge_sorted(a, b)
    assert result == sorted(result)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_length(a, b):
    result = merge_sorted(a, b)
    assert len(result) == len(a) + len(b)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_permutation(a, b):
    result = merge_sorted(a, b)
    assert sorted(result) == sorted(a + b)