from evolutionary_algorithm.evolutionary import Evolutionary
from move_strategies.strategies import MoveStrategy
from typing import Callable
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective
from checkers_and_minimax_python_module import MoveList


class UMDAc (Evolutionary):
    def __init__(self, selection_function: Callable, objective: Objective, population_size: int, descendant_size: int,
                 opponent_strategy: Callable[[MoveStrategy], MoveList], iters: int, n: int, **strategy_args):
        self.selection_function = selection_function
        super().__init__(objective, population_size, descendant_size, opponent_strategy, iters, n, **strategy_args)

    def select(self, values):
        return self.selection_function(self.coefficients_pawns, self.coefficients_kings, values, self.descendant_size, 2)

    def model_estimation(self, coefficients_pawns, coefficients_kings):
        self.mean = np.mean(coefficients_pawns, axis=0)
        self.deviation = np.std(coefficients_pawns, axis=0) * 0.9
        self.mean_kings = np.mean(coefficients_kings, axis=0)
        self.deviation_kings = np.std(coefficients_kings, axis=0) * 0.9


    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            # print(self.coefficients_pawns)
            selected_pawns, selected_kings = self.select(values)
            self.model_estimation(selected_pawns, selected_kings)
            self.random_coefficients()
            values = self.evaluate(i + 1, x)
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)]
