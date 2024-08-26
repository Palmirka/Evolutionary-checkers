from evolutionary_algorithm.evolutionary import Evolutionary
import random
from typing import Callable
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective


class PBILc(Evolutionary):
    def __init__(self, objective: Objective, population_size: int, descendant_size: int,
                 opponent_strategy: Callable[[MoveStrategy], MoveList], iters: int, n: int,
                 learning_rate: float, mutation_probability: float, disturbance_constant: float,
                 disturbance_probability: float, **strategy_args):
        self.learning_rate = learning_rate
        self.mutation_probability = mutation_probability
        self.disturbance_constant = disturbance_constant
        self.disturbance_probability = disturbance_probability
        super().__init__(objective, population_size, descendant_size, opponent_strategy, iters, n, **strategy_args)

    @staticmethod
    def binary_random(p):
        return int(random.uniform(0, 1) < p)

    def model_estimation(self, coefficients_pawns, coefficients_kings, coefficients_diff):
        best_pawn, second_best_pawn, worst_pawn = coefficients_pawns[-1], coefficients_pawns[-2], coefficients_pawns[0]
        best_king, second_best_king, worst_king = coefficients_kings[-1], coefficients_kings[-2], coefficients_kings[0]
        best_diff, second_best_diff, worst_diff = coefficients_diff[-1], coefficients_diff[-2], coefficients_diff[0]

        self.mean = self.mean * (1 - self.learning_rate) + (
                best_pawn + second_best_pawn - worst_pawn) * self.learning_rate
        disturbation_vector = np.array(
            [(random.uniform(0, 1) < self.mutation_probability) for _ in range(self.individual_length_pawns)])
        self.mean = (np.invert(disturbation_vector) * self.mean +
                     disturbation_vector * (self.mean * (1 - self.disturbance_probability) +
                                            self.binary_random(0.5) * self.disturbance_probability))
        self.deviation *= self.disturbance_constant

        self.mean_kings = self.mean_kings * (1 - self.learning_rate) + (
                best_king + second_best_king - worst_king) * self.learning_rate
        disturbation_vector = np.array(
            [(random.uniform(0, 1) < self.mutation_probability) for _ in range(self.individual_length_kings)])
        self.mean_kings = (np.invert(disturbation_vector) * self.mean_kings +
                           disturbation_vector * (self.mean_kings * (1 - self.disturbance_probability) +
                                                  self.binary_random(0.5) * self.disturbance_probability))
        self.deviation_kings *= self.disturbance_constant

        self.mean_diff = self.mean_diff * (1 - self.learning_rate) + (
                best_diff + second_best_diff - worst_diff) * self.learning_rate
        disturbation_vector = np.array(
            [(random.uniform(0, 1) < self.mutation_probability)])
        self.mean_diff = (np.invert(disturbation_vector) * self.mean_diff +
                          disturbation_vector * (self.mean_diff * (1 - self.disturbance_probability) +
                                                 self.binary_random(0.5) * self.disturbance_probability))
        self.deviation_diff *= self.disturbance_constant


    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        for i in range(self.iters):
            print(f'n: {x}, iter: {i}')
            self.model_estimation(self.coefficients_pawns[np.argsort(values)],
                                  self.coefficients_kings[np.argsort(values)], self.diff[np.argsort(values)])
            self.random_coefficients()
            if i % 10 == 5:
                self.show_iters(i, x)
            values = self.evaluate(i + 1, x)
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)]