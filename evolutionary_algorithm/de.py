from evolutionary_algorithm.evolutionary import Evolutionary
from move_strategies.strategies import MoveStrategy
from typing import Callable, Tuple
import numpy as np
from numpy.typing import NDArray
from evolutionary_algorithm.base_functions.objective import Objective
from checkers_and_minimax_python_module import MoveList
from evolutionary_algorithm.base_functions.mutation import Mutation
from evolutionary_algorithm.base_functions.crossover import Crossover
from evolutionary_algorithm.base_functions.selection import Selection


class DE (Evolutionary):
    def __init__(self, objective: Objective, population_size: int, games_for_iter: int,
                 opponent_strategy_list: NDArray[Tuple[Callable[[MoveStrategy], MoveList], int]], n: int,
                 mutation_factor: float, crossover_factor: float):
        self.mutation_factor = mutation_factor
        self.crossover_factor = crossover_factor
        super().__init__(objective=objective, population_size=population_size, games_for_iter=games_for_iter,
                         opponent_strategy_list=opponent_strategy_list, n=n)

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            if self.opponent_strategy_iters == 0:
                self.set_opponent_strategy()
                print('Switched to: ', self.opponent_strategy.__name__)
            mutated_pawns, mutated_kings, mutated_diff = Mutation.triple_combination(self.coefficients_pawns, self.mutation_factor), \
                Mutation.triple_combination(self.coefficients_kings, self.mutation_factor), \
                Mutation.triple_combination(self.coefficients_diff, self.mutation_factor)
            crossover_pawns, crossover_kings, crossover_diff = Crossover.combine_best(self.coefficients_pawns, mutated_pawns, self.crossover_factor), \
                Crossover.combine_best(self.coefficients_kings, mutated_kings, self.crossover_factor), \
                Crossover.combine_best(self.coefficients_diff, mutated_diff, self.crossover_factor)
            mutated_values = self.evaluate(i, x, crossover_pawns, crossover_kings, crossover_diff, False)
            self.coefficients_pawns, self.coefficients_kings, self.coefficients_diff = \
                Selection.replacement(self.coefficients_pawns, self.coefficients_kings, self.coefficients_diff,
                                      crossover_pawns, crossover_kings, crossover_diff, values, mutated_values)
            if i % 10 == 5:
                self.show_iters(i, x)
            values = self.evaluate(i + 1, x)
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)]