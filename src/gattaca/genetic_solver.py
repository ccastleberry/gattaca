import random
from enum import Enum
from typing import Type, TypeVar

import structlog

from gattaca.candidate_abc import Candidate
from gattaca.scorer import Scorer

logger = structlog.get_logger(__name__)
structlog.stdlib.recreate_defaults(log_level=None)


T = TypeVar("T", bound=Candidate)


class MutationScalingPattern(Enum):
    LINEAR = "linear"
    QUADRATIC = "quadratic"
    NONE = "none"


class GeneticSolver:
    def __init__(
        self,
        candidate_class: Type[T],
        scorer: Scorer[T],
        population_size: int = 100,
        generation_count: int = 100,
        keep_top_parents: bool = True,
        selection_percentage: float = 0.2,
        starting_mutation_count: int = 10,
        mutation_count_scaling: MutationScalingPattern = MutationScalingPattern.LINEAR,
        starting_mutation_scale: float = 1,
        mutation_scaling: MutationScalingPattern = MutationScalingPattern.LINEAR,
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
        self.starting_mutation_count = starting_mutation_count
        self.mutation_count_scaling = mutation_count_scaling
        self.starting_mutation_scale = starting_mutation_scale
        self.mutation_scaling = mutation_scaling

    def solve(self) -> Type[Candidate]:
        population = [
            self.candidate_class.generate_random() for _ in range(self.population_size)
        ]
        percent_step_per_loop = 1 / self.generation_count
        percent_remaining = 1.0
        for i in range(self.generation_count):
            log = logger.bind(generation=i + 1)

            # Get mutation count and scale
            mutation_count = self.get_mutation_count(percent_remaining)
            mutation_scale = self.get_mutation_scale(percent_remaining)
            log = log.bind(mutation_count=mutation_count, mutation_scale=mutation_scale)

            # TODO: add optimization so we don't re-score candidates
            population.sort(key=self.scorer.score)
            best_score = self.scorer.score(population[0])
            log = log.bind(best_score=best_score)
            # select only top of population
            selection_population = population[: self.selection_count]

            # initialize new population
            if self.keep_top_parents:
                new_population = selection_population
                refill_count = self.population_size - self.selection_count
            else:
                new_population = []
                refill_count = self.population_size

            # populate the new population
            for _ in range(refill_count):
                parent_1 = random.choice(selection_population)
                parent_2 = random.choice(selection_population)
                new_candidate = parent_1.crossover(other=parent_2)
                new_candidate.multi_mutate(scale=mutation_scale, count=mutation_count)
                new_population.append(new_candidate)

            # Update for next loop
            population = new_population
            percent_remaining = max(percent_remaining - percent_step_per_loop, 0)
            log.debug("Generation Complete", percent_remaining=percent_remaining)

        population.sort(key=self.scorer.score)
        return population[0]

    def get_mutation_count(self, gen_percent_remaining: float) -> int:
        if self.mutation_count_scaling == MutationScalingPattern.LINEAR:
            return round(self.starting_mutation_count * gen_percent_remaining)
        elif self.mutation_count_scaling == MutationScalingPattern.QUADRATIC:
            return round(self.starting_mutation_count * (gen_percent_remaining**2))
        elif self.mutation_count_scaling == MutationScalingPattern.NONE:
            return self.starting_mutation_count
        else:
            raise ValueError("No match for mutation_count_scaling found")

    def get_mutation_scale(self, gen_percent_remaining: float) -> float:
        if self.mutation_scaling == MutationScalingPattern.LINEAR:
            return self.starting_mutation_scale * gen_percent_remaining
        elif self.mutation_scaling == MutationScalingPattern.QUADRATIC:
            return self.starting_mutation_scale * (gen_percent_remaining**2)
        elif self.mutation_scaling == MutationScalingPattern.NONE:
            return self.starting_mutation_scale
        else:
            raise ValueError("No match for mutation_scaling found")
