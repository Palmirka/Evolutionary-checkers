from evolutionary_algorithm.evolutionary import Evolutionary
from move_strategies.strategies import MoveStrategy
from typing import Callable, Dict
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective
from checkers_and_minimax_python_module import MoveList


class UMDAc (Evolutionary):
    def __init__(self, selection_function: Callable, objective: Objective, population_size: int, descendant_size: int,
                 opponent_strategy: Callable[[MoveStrategy], MoveList], iters: int, n: int, **strategy_args):
        self.selection_function = selection_function
        super().__init__(objective, population_size, descendant_size, opponent_strategy, iters, n, **strategy_args)

    def select(self, values):
        return self.selection_function(self.coefficients, values, self.descendant_size, 2)

    def model_estimation(self, coefficients):
        self.mean = np.mean(coefficients, axis=0)
        self.deviation = np.std(coefficients, axis=0) * 0.9

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'n {x}')
        for i in range(self.iters):
            # print(f'n: {x}, iter: {i}')
            selected_coefficients = self.select(values)
            self.model_estimation(selected_coefficients)
            self.coefficients = self.random_coefficients()
            values = self.evaluate(i + 1, x)
        return self.coefficients[np.argmax(values)]
