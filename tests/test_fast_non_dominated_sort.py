from hypothesis import given, settings
from hypothesis import strategies as st

from gattaca.fast_non_dominated_sort import dominates, fast_non_dominated_sort


@st.composite
def list_of_tuple_floats(draw, tuple_len=st.integers(min_value=1, max_value=5)):
    tuple_len = draw(tuple_len)
    int_list = [st.floats() for _ in range(tuple_len)]
    return draw(st.lists(elements=st.tuples(*int_list), max_size=100, min_size=1))


@settings(max_examples=200)
@given(tuple_list=list_of_tuple_floats())
def test_sort_levels_dominate_correctly(tuple_list):
    pareto_fronts = fast_non_dominated_sort(tuple_list)
    pareto_len = len(pareto_fronts)
    assert pareto_len <= len(tuple_list)
    if pareto_len > 1:
        for i in range(pareto_len - 1):
            front_1 = pareto_fronts[i]
            front_2 = pareto_fronts[i + 1]
            for i_2 in front_2:
                assert any(
                    [dominates(tuple_list[i_1], tuple_list[i_2]) for i_1 in front_1]
                )
