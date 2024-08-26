from evolutionary_algorithm.evolutionary import Evolutionary
from move_strategies.strategies import MoveStrategy
from typing import Callable
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective
from checkers_and_minimax_python_module import MoveList
from evolutionary_algorithm.base_functions.mutation import Mutation
from evolutionary_algorithm.base_functions.crossover import Crossover
from evolutionary_algorithm.base_functions.selection import Selection


class DE (Evolutionary):
    def __init__(self, objective: Objective, population_size: int, opponent_strategy: Callable[[MoveStrategy], MoveList],
                 iters: int, n: int, mutation_factor: float, crossover_factor: float, **strategy_args):
        self.mutation_factor = mutation_factor
        self.crossover_factor = crossover_factor
        super().__init__(objective, population_size, 0, opponent_strategy, iters, n, **strategy_args)

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            mutated_pawns, mutated_kings, mutated_diff = Mutation.triple_combination(self.coefficients_pawns, self.mutation_factor), \
                Mutation.triple_combination(self.coefficients_kings, self.mutation_factor), \
                Mutation.triple_combination(self.diff, self.mutation_factor)
            crossover_pawns, crossover_kings, crossover_diff = Crossover.combine_best(self.coefficients_pawns, mutated_pawns, self.crossover_factor), \
                Crossover.combine_best(self.coefficients_kings, mutated_kings, self.crossover_factor), \
                Crossover.combine_best(self.diff, mutated_diff, self.crossover_factor)
            mutated_values = self.evaluate(i, x, crossover_pawns, crossover_kings, crossover_diff, False)
            self.coefficients_pawns, self.coefficients_kings, self.diff = \
                Selection.replacement(self.coefficients_pawns, self.coefficients_kings, crossover_pawns, crossover_kings, crossover_diff, values, mutated_values)
            values = self.evaluate(i + 1, x)
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)]