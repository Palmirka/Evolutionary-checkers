from evolutionary_algorithm.evolutionary_discrete import EvolutionaryDiscrete
from game.constants import POSSIBLE_VALUES, MAX_COEFFICIENT
from evolutionary_algorithm.base_functions.mutation import Mutation
from typing import Callable, List, Tuple, Dict
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
import numpy as np
from numpy.typing import NDArray
from evolutionary_algorithm.base_functions.objective import Objective


class PBIL(EvolutionaryDiscrete):
    def __init__(self, objective: Objective, population_size: int, games_for_iter: int,
                 opponent_strategy_list: NDArray[Tuple[Callable[[MoveStrategy], MoveList], int]], n: int,
                 learning_rate: float, mutation_probability: float, mutation_constant: float):
        self.learning_rate = learning_rate
        self.mutation_probability = mutation_probability
        self.mutation_constant = mutation_constant
        self.mutation_function = Mutation.random_value
        super().__init__(objective=objective, population_size=population_size, games_for_iter=games_for_iter,
                         opponent_strategy_list=opponent_strategy_list, n=n)

    def model_estimation(self, values, it):
        # starts with 2% ends with 15%
        best_percentage = 2 + (13*(it/self.iters))
        # starts with 5% ends with 0.1%
        # worst_percentage = 5 + (3 * (it/self.iters))

        # new_learning_rate = self.learning_rate - (0.9*self.learning_rate)*(it/self.iters)

        cut_value_point = (np.mean(values) + np.max(values))/2
        indices_above_cutpoint = np.where(values > cut_value_point)[0]
        # print(values)
        # print(np.array(values[indices_above_cutpoint]))
        sorted_values = np.argsort(values)

        mask = np.isin(sorted_values, indices_above_cutpoint)
        filtr = sorted_values[mask]
        # print(sorted_values)
        # print(filtr)

        sorted_pawns = self.coefficients_pawns[filtr]
        best_cut_size = int(best_percentage/100*self.population_size)
        if best_cut_size == 0:
            best_cut_size = 1
        best_pawns = sorted_pawns[-best_cut_size:][::-1]
        print("no. best pawns: ", int(best_cut_size))


        targets = np.zeros((self.individual_length_pawns, POSSIBLE_VALUES))
        for i in range(len(best_pawns)):
            targets[np.arange(self.individual_length_pawns), best_pawns[i] + MAX_COEFFICIENT] += 1
        self.probabilities = self.probabilities * (1 - self.learning_rate) + self.learning_rate*(targets)
        self.probabilities /= self.probabilities.sum(axis=1)[0]

        sorted_kings = self.coefficients_kings[filtr]
        best_kings = sorted_kings[-best_cut_size:][::-1]

        targets = np.zeros((self.individual_length_kings, POSSIBLE_VALUES))
        targets_worst = np.zeros((self.individual_length_kings, POSSIBLE_VALUES))
        for i in range(len(best_kings)):
            targets[np.arange(self.individual_length_kings), best_kings[i] + MAX_COEFFICIENT] += 1
        self.probabilities_kings = self.probabilities_kings * (1 - self.learning_rate) + self.learning_rate * (
                    targets - targets_worst)
        self.probabilities_kings /= self.probabilities_kings.sum(axis=1)[0]

        sorted_diff = self.diff[filtr]
        best_diff = sorted_diff[-best_cut_size:][::-1]

        targets = np.zeros((1, POSSIBLE_VALUES))
        targets_worst = np.zeros((1, POSSIBLE_VALUES))
        for i in range(len(best_diff)):
            targets[0][best_diff[i][0] + MAX_COEFFICIENT] += 1
        self.diff_probability = self.diff_probability * (1 - self.learning_rate) + self.learning_rate * (
                    targets - targets_worst)
        self.diff_probability /= self.diff_probability.sum(axis=1)[0]

        return best_pawns[0], best_kings[0], best_diff[0]

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            if self.opponent_strategy_iters == 0:
                self.set_opponent_strategy()
                print('Switched to: ', self.opponent_strategy.__name__)
            best_pawns, best_kings, best_diff = self.model_estimation(values, i)
            print(best_pawns[: 5], best_kings[: 5], best_diff)
            self.probabilities = self.mutation_function(self.probabilities, self.mutation_probability, self.mutation_constant, self.individual_length_pawns)
            self.probabilities_kings = self.mutation_function(self.probabilities_kings, self.mutation_probability,
                                                              self.mutation_constant, self.individual_length_kings)
            self.diff_probability = self.mutation_function(self.diff_probability, self.mutation_probability, self.mutation_constant, 1)
            self.random_coefficients(best_pawns, best_kings, best_diff)
            if i % 10 == 5:
                self.show_iters(i, x)
            values = self.evaluate(i + 1, x)
            self.opponent_strategy_iters -= 1
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)], self.diff[np.argmax(values)]
