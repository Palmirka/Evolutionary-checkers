import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
from game.play import Play
from game.constants import MAX_POINTS, MAX_COEFFICIENT, POSSIBLE_VALUES
from typing import Callable, Tuple, List
from numpy.typing import NDArray


class EvolutionaryDiscrete:
    def __init__(self, objective, population_size: int, games_for_iter: int,
                 opponent_strategy_list: NDArray[Tuple[Callable[[MoveStrategy], MoveList], int]], n: int):
        """Initialize evolutionary and diagram parameters"""
        self.pool = np.array([Engine() for _ in range(population_size)])
        self.individual_length_pawns = objective.size_p
        self.individual_length_kings = objective.size_k
        self.diff_probability = np.empty((1, POSSIBLE_VALUES), float)
        self.probabilities = np.empty((objective.size_p, POSSIBLE_VALUES), float)
        self.probabilities_kings = np.empty((objective.size_k, POSSIBLE_VALUES), float)
        self.opponent_strategy_list = opponent_strategy_list
        self.opponent_strategy = None
        self.opponent_strategy_iters = 0
        self.objective_function = objective.function
        self.coefficients_pawns = np.empty((population_size, objective.size_p), int)
        self.coefficients_kings = np.empty((population_size, objective.size_k), int)
        self.diff = np.empty(population_size, int)
        self.population_size = population_size
        self.games_for_iter = games_for_iter
        self.iters = sum(data[1] for data in self.opponent_strategy_list)
        self.n = n

        self.best_coefficients_pawns = np.empty((self.n, self.individual_length_pawns), int)
        self.best_coefficients_kings = np.empty((self.n, self.individual_length_kings), int)
        self.max_evaluations = np.empty((self.n, self.iters + 1), float)
        self.min_evaluations = np.empty((self.n, self.iters + 1), float)
        self.mean_evaluations = np.empty((self.n, self.iters + 1), float)

    def init(self):
        """Initialize starting values"""
        self.set_opponent_strategy()
        self.diff_probability.fill(1 / POSSIBLE_VALUES)
        self.probabilities.fill(1 / POSSIBLE_VALUES)
        self.probabilities_kings.fill(1 / POSSIBLE_VALUES)
        self.random_coefficients(np.random.randint(-10, 11, self.individual_length_pawns),
                                 np.random.randint(-10, 11, self.individual_length_kings),
                                 np.random.randint(-10, 11, 1))

    def set_opponent_strategy(self) -> None:
        (self.opponent_strategy, self.opponent_strategy_iters), self.opponent_strategy_list = \
            self.opponent_strategy_list[0], self.opponent_strategy_list[1:]

    def random_coefficients(self, best_pawns, best_kings, best_diff) -> None:
        """Generate coefficients with normal distribution"""

        def single_random(probabilities, length, debug=False):
            mask = np.random.random(length)
            cumulative = np.cumsum(probabilities, axis=1)
            if debug:
                print(mask)
                print('xd: ', cumulative)
                print(np.where(cumulative[0] > mask[0])[0][0])
            return np.array([np.where(cumulative[i] > mask[i])[0][0] - MAX_COEFFICIENT for i in range(length)])

        self.coefficients_pawns = np.array([single_random(self.probabilities, self.individual_length_pawns)
                                            for _ in range(self.population_size - 1)] + [best_pawns])
        self.coefficients_kings = np.array([single_random(self.probabilities_kings, self.individual_length_kings)
                                            for _ in range(self.population_size - 1)] + [best_kings])
        self.diff = np.array([single_random(self.diff_probability, 1)
                              for _ in range(self.population_size - 1)] + [best_diff])

    def model_estimation(self, values, idx):
        """Estimate probability parameters to generate better population"""
        pass

    def evaluate(self, i: int, x: int, pawns: np.ndarray = None, kings: np.ndarray = None, save: bool = True) -> np.ndarray:
        """Get and save new fitness values"""
        def evaluate_individual(idx, pawns, kings):
            self.pool[idx].reset()
            return idx, Play(self.pool[idx], pawns[idx], kings[idx], self.diff[idx], self.objective_function, self.opponent_strategy).play(idx, self.games_for_iter)

        if pawns is None:
            pawns = self.coefficients_pawns
        if kings is None:
            kings = self.coefficients_kings

        values = np.zeros(self.population_size)
        # for idx in range(self.population_size):
        #     _, values[idx] = evaluate_individual(idx, pawns, kings)
        results = Parallel(n_jobs=-1)(
            delayed(evaluate_individual)(idx, pawns, kings) for idx in range(self.population_size))

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

    def run_n_times(self) -> Tuple[np.ndarray, np.ndarray]:
        """Save results from n runs of function"""
        for x in range(self.n):
            self.best_coefficients_pawns[x], self.best_coefficients_kings[x] = self.run(x)
        return self.best_coefficients_pawns, self.best_coefficients_kings

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