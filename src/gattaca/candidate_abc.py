from abc import ABC, abstractmethod
from typing import Any


class Candidate(ABC):
    @classmethod
    @abstractmethod
    def generate_random(cls):
        """Generate a new random instance of this candidate"""
        raise NotImplementedError

    @abstractmethod
    def mutate(self, scale: float = 1) -> None:
        """mutates this candidate in place."""
        raise NotImplementedError

    def multi_mutate(self, scale: float = 1, count: int = 5):
        """mutates candidate in place multiple times"""
        for _ in range(count):
            self.mutate(scale=scale)

    @abstractmethod
    def crossover(self, other):
        """Crosses this candiate with another to get a new candidate"""
        raise NotImplementedError

    @abstractmethod
    def solution(self) -> Any:
        """Return solution from candidate"""
        raise NotImplementedError
