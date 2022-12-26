from abc import ABC, abstractmethod
from typing import Self


class Candidate(ABC):
    @classmethod
    @abstractmethod
    def generate_random(cls) -> Self:
        raise NotImplementedError

    @abstractmethod
    def mutate(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def crossover(self, other: Self) -> Self:
        raise NotImplementedError

