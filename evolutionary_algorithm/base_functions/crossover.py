import numpy as np


class Crossover:
    """Placeholder for crossover functions"""

    @staticmethod
    def combine_best(population: np.ndarray, mutants: np.ndarray, crossover_factor: float):
        # def single_cross(individual: np.ndarray, mutant: np.ndarray):
        #     crossed = np.random.rand(individual.size) < crossover_factor
        #     crossed_individual = np.where(crossed, mutant, individual)
        #     return crossed_individual
        #
        # crossed_population = np.array(
        #     [single_cross(population[idx], mutants[idx]) for idx in range(population.shape[0])])
        crossover_mask = np.random.rand(*population.shape) < crossover_factor
        crossed_population = np.where(crossover_mask, mutants, population)
        return crossed_population
