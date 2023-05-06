import random
from typing import Dict, List, Set, Tuple


def dominates(a: Tuple[float, ...], b: Tuple[float, ...]) -> bool:
    # return true if all values are lteq and at least one is lt.
    all_bool = all([a[i] <= b[i] for i in range(len(a))])
    any_bool = any([a[i] < b[i] for i in range(len(a))])
    return all_bool and any_bool


def pareto_front_sampler_random(points: List, sample_count: int) -> List:
    if len(points) < sample_count:
        return points
    else:
        return random.sample(population=points, k=sample_count)


def fast_non_dominated_sort(points: List[Tuple[float, ...]]) -> List[List[int]]:
    fronts: List[List[int]] = [[]]
    s_p_dict: Dict[int, Set[int]] = dict()
    n_p_dict = dict()
    for i, p in enumerate(points):
        s_p_dict[i] = set()
        n_p_dict[i] = 0
        for j, q in enumerate(points):
            if dominates(p, q):
                s_p_dict[i].add(j)
            elif dominates(q, p):
                n_p_dict[i] += 1
        if n_p_dict[i] == 0:
            fronts[0].append(i)
    front_index = 0
    while len(fronts[front_index]) > 0:
        new_front = list()
        for i in fronts[front_index]:
            for j in s_p_dict[i]:
                n_p_dict[j] -= 1
                if n_p_dict[j] == 0:
                    new_front.append(j)
        front_index += 1
        fronts.append(new_front)
    fronts.pop(-1)
    return fronts
