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


def main():
    scorer = Scorer(
        SingleValueCandidate,
        scoring_function=scoring_function,
        scoring_direction=ScoringDirection.MIN,
    )
    solver = GeneticSolver(
        population_size=200,
        generation_count=1000,
        candidate_class=SingleValueCandidate,
        scorer=scorer,
    )
    return solver.solve()


if __name__ == "__main__":
    solution = main()
    print(solution.value)
