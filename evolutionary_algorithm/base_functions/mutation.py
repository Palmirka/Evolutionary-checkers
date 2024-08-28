from random import random
import numpy as np
from typing import Callable
from game.constants import POSSIBLE_VALUES, MAX_COEFFICIENT


class Mutation:
    """Class of all available mutation functions"""

    @staticmethod
    def base(probability: float, individual: np.ndarray, function: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
        """Returns mutated individual by function with given probability"""
        if random.uniform(0, 1) < probability:
            return function(individual)
        return individual

    @staticmethod
    def triple_combination(population: np.ndarray, mutation_factor: float):
        mutated_population = np.empty_like(population)
        indices = np.arange(population.shape[0])
        for idx in range(population.shape[0]):
            selected_indices = np.random.choice(np.delete(indices, idx), 3, replace=False)
            a, b, c = population[selected_indices]
            mutated_population[idx] = a + mutation_factor * (b - c)
        return mutated_population

    @staticmethod
    def random_value(probabilities: np.ndarray, mutation_probability: float,  mutation_constant: float, individual_length):
        for j in range(individual_length):
            if np.random.random() < mutation_probability:
                for value in range(MAX_COEFFICIENT):
                    probabilities[j][value] = probabilities[j][value] * (1 - mutation_constant) + mutation_constant * np.random.random()
                probabilities[j] /= probabilities[j].sum()
        return probabilities
