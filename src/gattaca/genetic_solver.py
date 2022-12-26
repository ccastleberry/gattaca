from gattaca.candidate_abc import Candidate
from typing import Type, TypeVar, Callable

T = TypeVar("T", bound=Type[Candidate])

class GeneticSolver():

    def __init__(
            self,
            population_size: int,
            generation_count: int,
            candidate_class: T,
            score_function: Callable[[T], float]
    ):
        self.population_size = population_size
        self.generation_count = generation_count
        self.candidate_class = candidate_class
        self.score_function = score_function

    def solve(self) -> T:
        starting_population = [
            self.candidate_class.generate_random() for _ in range(self.population_size)
        ]
        starting_population.sort(
            key=self.score_function
        )
        return starting_population[0]
