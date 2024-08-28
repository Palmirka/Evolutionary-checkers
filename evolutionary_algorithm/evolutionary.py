import numpy as np
import pickle
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
from game.play import Play
from game.constants import MAX_POINTS, POSSIBLE_VALUES
from typing import Callable, Tuple
from numpy.typing import NDArray

class Evolutionary:
    def __init__(self, objective, population_size: int, games_for_iter: int,
                 opponent_strategy_list: NDArray[Tuple[Callable[[MoveStrategy], MoveList], int]], n: int):
        """Initialize evolutionary and diagram parameters"""
        self.pool = np.array([Engine() for _ in range(population_size)])
        self.individual_length_pawns = objective.size_p
        self.individual_length_kings = objective.size_k
        self.mean = None
        self.deviation = None
        self.mean_kings = None
        self.deviation_kings = None
        self.mean_diff = None
        self.deviation_diff = None
        self.probabilities_kings = np.empty((objective.size_k, POSSIBLE_VALUES), float)
        self.opponent_strategy_list = opponent_strategy_list
        self.opponent_strategy = None
        self.opponent_strategy_iters = 0
        self.objective_function = objective.function
        self.coefficients_pawns = np.empty((population_size, objective.size_p), float)
        self.coefficients_kings = np.empty((population_size, objective.size_k), float)
        self.diff = np.empty((population_size, 1), float)
        self.population_size = population_size
        self.games_for_iter = games_for_iter
        self.iters = sum(data[1] for data in self.opponent_strategy_list)
        self.n = n

        self.best_coefficients_pawns = np.empty((self.n, self.individual_length_pawns), float)
        self.best_coefficients_kings = np.empty((self.n, self.individual_length_kings), float)
        self.best_diff = np.empty((self.n, 1), float)
        self.max_evaluations = np.empty((self.n, self.iters + 1), float)
        self.min_evaluations = np.empty((self.n, self.iters + 1), float)
        self.mean_evaluations = np.empty((self.n, self.iters + 1), float)

    def init(self):
        """Initialize starting values"""
        self.set_opponent_strategy()
        self.mean = np.zeros(self.individual_length_pawns)
        self.deviation = np.ones(self.individual_length_pawns)
        self.mean_kings = np.zeros(self.individual_length_kings)
        self.deviation_kings = np.ones(self.individual_length_kings)
        self.mean_diff = np.zeros(1)
        self.deviation_diff = np.ones(1)
        self.random_coefficients()

    def set_opponent_strategy(self) -> None:
        (self.opponent_strategy, self.opponent_strategy_iters), self.opponent_strategy_list = \
            self.opponent_strategy_list[0], self.opponent_strategy_list[1:]

    def random_coefficients(self) -> None:
        """Generate coefficients with normal distribution"""

        def single_random(mean, deviation, length):
            return np.array([np.random.normal(mean[i], deviation[i]) for i in range(length)])

        self.coefficients_pawns = np.array([single_random(self.mean, self.deviation, self.individual_length_pawns)
                                            for _ in range(self.population_size)])
        self.coefficients_kings = np.array(
            [single_random(self.mean_kings, self.deviation_kings, self.individual_length_kings)
             for _ in range(self.population_size)])
        np.random.normal(self.mean_diff[0], self.deviation_diff[0])
        self.diff = np.array(
            [single_random(self.mean_diff, self.deviation_diff, 1) for _ in range(self.population_size)])

    def model_estimation(self, coefficient_pawns, coefficient_kings, idx):
        """Estimate probability parameters to generate better population"""
        pass

    def evaluate(self, i: int, x: int, pawns: np.ndarray = None, kings: np.ndarray = None,
                 diff: np.ndarray = None, save: bool = True) -> np.ndarray:
        """Get and save new fitness values"""

        def evaluate_individual(idx, pawns, kings, diff):
            self.pool[idx].reset()
            return idx, Play(self.pool[idx], pawns[idx], kings[idx], diff[idx], self.objective_function,
                             self.opponent_strategy).play(idx, self.games_for_iter)

        if pawns is None:
            pawns = self.coefficients_pawns
        if kings is None:
            kings = self.coefficients_kings
        if diff is None:
            diff = self.diff

        values = np.zeros(self.population_size)
        # for idx in range(self.population_size):
        #     _, values[idx] = evaluate_individual(idx, pawns, kings, diff)
        results = Parallel(n_jobs=-1)(
            delayed(evaluate_individual)(idx, pawns, kings, diff) for idx in range(self.population_size))

        for idx, value in results:
            values[idx] = value
        if save:
            self.max_evaluations[x][i] = np.max(values)
            self.min_evaluations[x][i] = np.min(values)
            self.mean_evaluations[x][i] = np.mean(values)
        return values

    def run(self, x) -> np.ndarray:
        """Single run of experiment"""
        pass

    def run_n_times(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Save results from n runs of function"""

        for x in range(self.n):
            self.best_coefficients_pawns[x], self.best_coefficients_kings[x], self.best_diff[x] = self.run(x)
        return self.best_coefficients_pawns, self.best_coefficients_kings, self.best_diff
    
    def save(self):
        results = {
            'pawns': self.best_coefficients_pawns,
            'kings': self.best_coefficients_kings,
            'diff' : self.best_diff
        }
        with open('results.txt', 'wb') as handle:
            pickle.dump(results, handle)

    def show(self):
        """Show evaluation of fitness function"""
        plt.figure()
        plt.title(self.__class__.__name__)
        plt.plot([MAX_POINTS] * (self.iters + 1), color='r')
        plt.plot([-MAX_POINTS] * (self.iters + 1), color='r')
        plt.plot(np.mean(self.max_evaluations, axis=0), label='max_evaluation')
        plt.plot(np.mean(self.min_evaluations, axis=0), label='min_evaluation')
        plt.plot(np.mean(self.mean_evaluations, axis=0), label='mean_evaluation')
        plt.legend()
        plt.show()

    def show_iters(self, iter, n):
        plt.figure()
        plt.title(f'{self.__class__.__name__}, n = {n}, iter = {iter}')
        plt.plot([-MAX_POINTS] * (self.iters + 1), color='r')
        plt.plot([MAX_POINTS] * (self.iters + 1), color='r')
        plt.plot(np.mean(self.max_evaluations[:n+1, :iter+1], axis=0), label='max_evaluation')
        plt.plot(np.mean(self.min_evaluations[:n+1, :iter+1], axis=0), label='min_evaluation')
        plt.plot(np.mean(self.mean_evaluations[:n+1, :iter+1], axis=0), label='mean_evaluation')
        plt.legend()
        plt.show()
