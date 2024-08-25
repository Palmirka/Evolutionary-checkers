import numpy as np
import random


class Crossover:
    """Placeholder for crossover functions"""

    @staticmethod
    def combine_best(population: np.ndarray, mutants: np.ndarray, crossover_factor: float):
        def single_cross(individual: np.ndarray, mutant: np.ndarray):
            crossed = []
            for idx in range(individual.size):
                if random.uniform(0, 1) < crossover_factor:
                    crossed.append(mutant[idx])
                else:
                    crossed.append(individual[idx])
            return crossed

        crossed_population = np.array(
            [single_cross(population[idx], mutants[idx]) for idx in range(population.shape[0])])
        return crossed_population
