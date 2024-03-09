from random import random
from numpy import ndarray
from typing import Callable


class Mutation:
    """Class of all available mutation functions"""

    @staticmethod
    def base(probability: float, individual: ndarray, function: Callable[[ndarray], ndarray]) -> ndarray:
        """Returns mutated individual by function with given probability"""
        if random.uniform(0, 1) < probability:
            return function(individual)
        return individual
