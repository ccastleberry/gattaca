from abc import ABC, abstractmethod


class Candidate(ABC):
    @classmethod
    @abstractmethod
    def generate_random(cls):
        raise NotImplementedError

    @abstractmethod
    def mutate(self):
        raise NotImplementedError

    @abstractmethod
    def crossover(self, other):
        raise NotImplementedError
