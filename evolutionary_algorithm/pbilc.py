from evolutionary_algorithm.evolutionary import Evolutionary
import random
from typing import Callable, Tuple
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective
from numpy.typing import NDArray


class PBILc(Evolutionary):
    def __init__(self, objective: Objective, population_size: int, games_for_iter: int,
                 opponent_strategy_list: NDArray[Tuple[Callable[[MoveStrategy], MoveList], int]], n: int,
                 learning_rate: float, mutation_probability: float, disturbance_probability: float,
                 deviation_constant: float):
        self.learning_rate = learning_rate
        self.mutation_probability = mutation_probability
        self.disturbance_probability = disturbance_probability
        self.deviation_constant = deviation_constant
        super().__init__(objective=objective, population_size=population_size, games_for_iter=games_for_iter,
                         opponent_strategy_list=opponent_strategy_list, n=n)

    @staticmethod
    def binary_random(p):
        return int(random.uniform(0, 1) < p)

    def model_estimation(self, coefficients_pawns, coefficients_kings, coefficients_diff):
        best_percentage = 7
        best_pawn, second_best_pawn, worst_pawn = coefficients_pawns[-1], coefficients_pawns[-2], coefficients_pawns[0]
        best_king, second_best_king, worst_king = coefficients_kings[-1], coefficients_kings[-2], coefficients_kings[0]
        best_diff, second_best_diff, worst_diff = coefficients_diff[-1], coefficients_diff[-2], coefficients_diff[0]

        best_to_cut = int(best_percentage / 100 * self.population_size)
        print("no. elite pawns: ", best_to_cut)
        target_pawns = np.sum(coefficients_pawns[-best_to_cut:])
        target_kings = np.sum(coefficients_kings[-best_to_cut:])
        target_diff = np.sum(coefficients_diff[-best_to_cut:])

        def single_model(mean, target, deviation, individual_length):
            mean = mean * (1 - self.learning_rate) + target * self.learning_rate
            disturbation_vector = np.random.rand(individual_length) < self.mutation_probability
            mean = np.where(disturbation_vector,
                            mean * (1 - self.disturbance_probability) + (
                                        random.random() < 0.5) * self.disturbance_probability,
                            mean)
            deviation *= self.deviation_constant
            return mean, deviation

        self.mean, self.deviation = single_model(self.mean, target_pawns, self.deviation, self.individual_length_pawns)
        self.mean_kings, self.deviation_kings = single_model(self.mean_kings, target_kings, self.deviation_kings, self.individual_length_kings)
        self.mean_diff, self.deviation_diff = single_model(self.mean_diff, target_diff, self.deviation_diff, 1)

        # self.mean = self.mean * (1 - self.learning_rate) + target_pawns * self.learning_rate
        # disturbation_vector = np.array(
        #     [(random.uniform(0, 1) < self.mutation_probability) for _ in range(self.individual_length_pawns)])
        # self.mean = (np.invert(disturbation_vector) * self.mean +
        #              disturbation_vector * (self.mean * (1 - self.disturbance_probability) +
        #                                     self.binary_random(0.5) * self.disturbance_probability))
        # self.deviation *= self.disturbance_constant
        #
        # self.mean_kings = self.mean_kings * (1 - self.learning_rate) + (
        #         target_kings) * self.learning_rate
        # disturbation_vector = np.array(
        #     [(random.uniform(0, 1) < self.mutation_probability) for _ in range(self.individual_length_kings)])
        # self.mean_kings = (np.invert(disturbation_vector) * self.mean_kings +
        #                    disturbation_vector * (self.mean_kings * (1 - self.disturbance_probability) +
        #                                           self.binary_random(0.5) * self.disturbance_probability))
        # self.deviation_kings *= self.disturbance_constant
        #
        # self.mean_diff = self.mean_diff * (1 - self.learning_rate) + (
        #         target_diff) * self.learning_rate
        # disturbation_vector = np.array(
        #     [(random.uniform(0, 1) < self.mutation_probability)])
        # self.mean_diff = (np.invert(disturbation_vector) * self.mean_diff +
        #                   disturbation_vector * (self.mean_diff * (1 - self.disturbance_probability) +
        #                                          self.binary_random(0.5) * self.disturbance_probability))
        # self.deviation_diff *= self.disturbance_constant

        return best_pawn, best_king, best_diff

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            if self.opponent_strategy_iters == 0:
                self.set_opponent_strategy()
                print('Switched to: ', self.opponent_strategy.__name__)
            best_pawn, best_king, best_diff = self.model_estimation(self.coefficients_pawns[np.argsort(values)],
                                                                    self.coefficients_kings[np.argsort(values)],
                                                                    self.diff[np.argsort(values)])
            self.random_coefficients(best_pawn, best_king, best_diff)
            if i % 10 == 5:
                self.show_iters(i, x)
            values = self.evaluate(i + 1, x)
            self.opponent_strategy_iters -= 1
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)], self.diff[
            np.argmax(values)]
