from evolutionary_algorithm.evolutionary import Evolutionary
from move_strategies.strategies import MoveStrategy
from typing import Callable, Tuple
from checkers.game import Game
import numpy as np


class UMDAc (Evolutionary):
    def __init__(self, selection_function, objective_function: Callable[[Game, np.ndarray], float], population_size: int,
                 descendant_size: int, opponent_strategy: Callable[[MoveStrategy], Tuple[int, int]], iters: int, n: int,
                 individual_length=12):
        self.selection_function = selection_function
        super().__init__(objective_function, population_size, descendant_size, opponent_strategy, iters, n,
                         individual_length)

    def select(self, values):
        return self.selection_function(self.coefficients, values, self.descendant_size, 2)

    def model_estimation(self, coefficients):
        self.mean = np.mean(coefficients, axis=0)
        self.deviation = np.std(coefficients, axis=0) * 0.9

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        for i in range(self.iters):
            selected_coefficients = self.select(values)
            self.model_estimation(selected_coefficients)
            self.coefficients = self.random_coefficients()
            values = self.evaluate(i + 1, x)
        return self.coefficients[np.argmax(values)]
