from typing import TypeVar, Type, Generic, Callable
from enum import Enum

from gattaca.candidate_abc import Candidate

T = TypeVar("T", bound=Candidate)


class ScoringDirection(Enum):
    MIN = "min"
    MAX = "max"


class Scorer(Generic[T]):

    def __init__(
            self,
            candidate_class: Type[T],
            scoring_function: Callable[[T], float],
            scoring_direction: ScoringDirection = ScoringDirection.MIN
    ):
        self.candidate_class = candidate_class
        self.scoring_function = scoring_function
        self.scoring_direction = scoring_direction


    def score(self, candidate: T) -> float:
        if self.scoring_direction == ScoringDirection.MIN:
            return self.scoring_function(candidate)
        return self.scoring_function(candidate) * -1


