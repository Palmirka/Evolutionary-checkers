import numpy as np


class Crossover:
    """Placeholder for crossover functions"""

    @staticmethod
    def combine_best(population: np.ndarray, mutants: np.ndarray, crossover_factor: float):
        crossover_mask = np.random.rand(*population.shape) < crossover_factor
        crossed_population = np.where(crossover_mask, mutants, population)
        return crossed_population
