import random

from gattaca.candidate_abc import Candidate
from gattaca.genetic_solver import GeneticSolver
from gattaca.scorer import Scorer, ScoringDirection


# Define the Candidate class
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


# Define Scoring function
def scoring_function(candidate: SingleValueCandidate) -> float:
    x = candidate.value
    return (3 - x) ** 2

scorer = Scorer(
        SingleValueCandidate,
        scoring_function=scoring_function,
        scoring_direction=ScoringDirection.MIN,
    )
def solve(pop: int, gen: int):
    solver = GeneticSolver(
        population_size=pop,
        generation_count=gen,
        candidate_class=SingleValueCandidate,
        scorer=scorer,
    )
    solver.solve()

def solve_with_pop_10_gen_10():
    solve(10, 10)

def solve_with_pop_100_gen_10():
    solve(100, 10)

def solve_with_pop_10_gen_100():
    solve(10, 100)


__benchmarks__ = [
    (solve_with_pop_100_gen_10, solve_with_pop_10_gen_10, "pop:100/gen:10 vs pop:10/gen:10"),
    (solve_with_pop_10_gen_100, solve_with_pop_10_gen_10, "pop:10/gen:100 vs pop:10/gen:10"),
]