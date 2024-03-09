from evolutionary_algorithm.evolutionary import Evolutionary
import random
from typing import Callable, Tuple
from checkers.game import Game
from move_strategies.strategies import MoveStrategy
import numpy as np


class PBILc(Evolutionary):
    def __init__(self, objective_function: Callable[[Game, np.ndarray], float], population_size: int,
                 descendant_size: int, opponent_strategy: Callable[[MoveStrategy], Tuple[int, int]], iters: int, n: int,
                 learning_rate: float, mutation_probability: float, disturbance_constant: float,
                 disturbance_probability: float, individual_length=12):
        self.learning_rate = learning_rate
        self.mutation_probability = mutation_probability
        self.disturbance_constant = disturbance_constant
        self.disturbance_probability = disturbance_probability
        super().__init__(objective_function, population_size, descendant_size, opponent_strategy, iters, n,
                         individual_length)

    @staticmethod
    def binary_random(p):
        return int(random.uniform(0, 1) < p)

    def model_estimation(self, coefficients):
        best_individual, second_best_individual = coefficients[-1], coefficients[-2]
        worst_individual = coefficients[0]
        self.mean = self.mean * (1 - self.learning_rate) + (
                    best_individual + second_best_individual - worst_individual) * self.learning_rate
        disturbation_vector = np.array(
            [(random.uniform(0, 1) < self.mutation_probability) for _ in range(self.individual_length)])
        self.mean = (np.invert(disturbation_vector) * self.mean +
                     disturbation_vector * (self.mean * (1 - self.disturbance_probability) +
                                            self.binary_random(0.5) * self.disturbance_probability))
        self.deviation *= self.disturbance_constant

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        for i in range(self.iters):
            self.model_estimation(self.coefficients[np.argsort(values)])
            self.coefficients = self.random_coefficients()
            values = self.evaluate(i + 1, x)
        return self.coefficients[np.argmax(values)]
