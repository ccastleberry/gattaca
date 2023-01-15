import random
from typing import Callable, Type, TypeVar

from gattaca.candidate_abc import Candidate
from gattaca.scorer import Scorer, ScoringDirection

T = TypeVar("T", bound=Type[Candidate])


class GeneticSolver:
    def __init__(
        self,
        candidate_class: T,
        scorer: Scorer[T],
        population_size: int = 100,
        generation_count: int = 100,
        keep_top_parents: bool = True,
        selection_percentage: float = 0.2,
    ):
        # TODO: Write validation function and tests
        if population_size < 0:
            raise ValueError("population_size must be greater than 0.")
        if generation_count < 0:
            raise ValueError("generation_count must be greater than 0.")
        if selection_percentage > 1 or selection_percentage < 0:
            raise ValueError("selection_percentage must be between 0 and 1.")
        self.population_size = population_size
        self.generation_count = generation_count
        self.candidate_class = candidate_class
        self.scorer = scorer
        self.keep_top_parents = keep_top_parents
        self.selection_percentage = selection_percentage
        self.selection_count = round(population_size * selection_percentage)

    def solve(self) -> Type[Candidate]:
        population = [
            self.candidate_class.generate_random() for _ in range(self.population_size)
        ]
        for _ in range(self.generation_count):
            # TODO: add optimization so we don't re-score candidates
            population.sort(key=self.scorer.score)
            top_population = population[: self.selection_count]
            for _ in range(self.population_size - self.selection_count):
                parent_1 = random.choice(top_population)
                parent_2 = random.choice(top_population)
                new_candidate = parent_1.crossover(other=parent_2)
                mutated_candidate = new_candidate.mutate()
                top_population.append(mutated_candidate)
            population = top_population

        population.sort(key=self.scorer.score)
        return population[0]
