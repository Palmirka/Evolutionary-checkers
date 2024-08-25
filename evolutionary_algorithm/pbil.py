from evolutionary_algorithm.evolutionary_discrete import EvolutionaryDiscrete
from game.constants import POSSIBLE_VALUES, MAX_COEFFICIENT
from evolutionary_algorithm.base_functions.mutation import Mutation
from typing import Callable
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective


class PBIL(EvolutionaryDiscrete):
    def __init__(self, objective: Objective, population_size: int, descendant_size: int,
                 opponent_strategy: Callable[[MoveStrategy], MoveList], iters: int, n: int,
                 learning_rate: float, mutation_probability: float, mutation_constant: float,
                 **strategy_args):
        self.learning_rate = learning_rate
        self.mutation_probability = mutation_probability
        self.mutation_constant = mutation_constant
        self.mutation_function = Mutation.random_value
        super().__init__(objective, population_size, descendant_size, opponent_strategy, iters, n, **strategy_args)

    def model_estimation(self, values):
        best_pawns = self.coefficients_pawns[np.argmax(values)]
        targets = np.zeros((self.individual_length_pawns, POSSIBLE_VALUES))
        for idx in range(self.individual_length_pawns):
            targets[idx][best_pawns[idx] + MAX_COEFFICIENT] = 1
        self.probabilities = self.probabilities * (1 - self.learning_rate) + self.learning_rate * targets
        self.probabilities /= self.probabilities.sum(axis=1)[0]

        best_kings = self.coefficients_kings[np.argmax(values)]
        targets = np.zeros((self.individual_length_kings, POSSIBLE_VALUES))
        for idx in range(self.individual_length_kings):
            targets[idx][best_kings[idx] + MAX_COEFFICIENT] = 1
        self.probabilities_kings = self.probabilities_kings * (1 - self.learning_rate) + self.learning_rate * targets
        self.probabilities_kings /= self.probabilities_kings.sum(axis=1)[0]

        best_diff = self.diff[np.argmax(values)]

        targets = np.zeros((1, POSSIBLE_VALUES))
        targets[0][best_diff[0] + MAX_COEFFICIENT] = 1
        self.diff_probability = self.diff_probability * (1 - self.learning_rate) + self.learning_rate * targets
        self.diff_probability /= self.diff_probability.sum(axis=1)[0]

        return best_pawns, best_kings, best_diff

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            best_pawns, best_kings, best_diff = self.model_estimation(values)
            print(best_pawns[: 5], best_kings[: 5], best_diff)
            self.probabilities = self.mutation_function(self.probabilities, self.mutation_probability, self.mutation_constant, self.individual_length_pawns)
            self.probabilities_kings = self.mutation_function(self.probabilities_kings, self.mutation_probability,
                                                              self.mutation_constant, self.individual_length_kings)
            self.diff_probability = self.mutation_function(self.diff_probability, self.mutation_probability, self.mutation_constant, 1)
            self.random_coefficients(best_pawns, best_kings, best_diff)
            if i % 10 == 5:
                self.show_iters(i, x)
            values = self.evaluate(i + 1, x)
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)]
