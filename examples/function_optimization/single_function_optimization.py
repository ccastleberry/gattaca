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

    def mutate(self, scale: float = 1):
        new_value = self.value + random.normalvariate(0, 5) * scale
        return SingleValueCandidate(value=new_value)

    def crossover(self, other):
        new_value = (self.value + other.value) / 2
        return SingleValueCandidate(value=new_value)

    def solution(self) -> float:
        return self.value


# Define Scoring function
def scoring_function(candidate: SingleValueCandidate) -> float:
    x = candidate.value
    return (17 - x) ** 2


def main():
    scorer = Scorer(
        SingleValueCandidate,
        scoring_function=scoring_function,
        scoring_direction=ScoringDirection.MIN,
    )
    solver = GeneticSolver(
        population_size=200,
        generation_count=100,
        candidate_class=SingleValueCandidate,
        scorer=scorer,
        selection_percentage=0.2,
        keep_top_parents=False,
    )
    return solver.solve()


if __name__ == "__main__":
    best_candidate = main()
    solution = best_candidate.solution()
    print(f"{solution=}")
