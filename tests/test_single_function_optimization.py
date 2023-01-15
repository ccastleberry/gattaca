import random

import pytest

from gattaca.candidate_abc import Candidate
from gattaca.genetic_solver import GeneticSolver
from gattaca.scorer import Scorer, ScoringDirection


class SingleValueCandidate(Candidate):
    def __init__(self, value: float):
        self.value = value

    @classmethod
    def generate_random(cls):
        return SingleValueCandidate(value=random.uniform(-100, 101))

    def mutate(self):
        new_value = self.value + random.normalvariate(0, 5)
        return SingleValueCandidate(value=new_value)

    def crossover(self, other):
        new_value = (self.value + other.value) / 2
        return SingleValueCandidate(value=new_value)


@pytest.fixture(scope="session")
def single_value_scorer_min():
    def scoring_function(candidate: SingleValueCandidate) -> float:
        x = candidate.value
        return (3 - x) ** 2

    scorer = Scorer(
        SingleValueCandidate,
        scoring_function=scoring_function,
        scoring_direction=ScoringDirection.MIN,
    )
    return scorer


@pytest.fixture(scope="session")
def single_value_scorer_max():
    def scoring_function(candidate: SingleValueCandidate) -> float:
        x = candidate.value
        return -((3 - x) ** 2)

    scorer = Scorer(
        SingleValueCandidate,
        scoring_function=scoring_function,
        scoring_direction=ScoringDirection.MAX,
    )
    return scorer


def test_single_value_example_runs_min(single_value_scorer_min):
    solver = GeneticSolver(
        population_size=20,
        generation_count=20,
        candidate_class=SingleValueCandidate,
        scorer=single_value_scorer_min,
    )
    solution = solver.solve()
    assert abs(solution.value - 3) < 0.1


def test_single_value_example_runs_max(single_value_scorer_max):
    solver = GeneticSolver(
        population_size=20,
        generation_count=20,
        candidate_class=SingleValueCandidate,
        scorer=single_value_scorer_max,
    )
    solution = solver.solve()
    assert abs(solution.value - 3) < 0.1
