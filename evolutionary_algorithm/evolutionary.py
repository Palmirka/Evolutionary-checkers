import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from checkers.game import Game
from move_strategies.strategies import MoveStrategy
from game.constants import titles
from game.play import Play
from typing import Callable, Tuple


class Evolutionary:
    def __init__(self, objective_function: Callable[[Game, np.ndarray], float], population_size: int,
                 descendant_size: int, opponent_strategy: Callable[[MoveStrategy], Tuple[int, int]], iters: int, n: int,
                 individual_length=12):
        """Initialize evolutionary and diagram parameters"""
        self.mean = None
        self.deviation = None
        self.opponent_strategy = opponent_strategy
        self.objective_function = objective_function
        self.coefficients = np.empty((population_size, individual_length))
        self.population_size = population_size
        self.descendant_size = descendant_size
        self.individual_length = individual_length
        self.iters = iters
        self.n = n

        self.best_coefficients = np.empty((self.n, self.individual_length))
        self.max_evaluations = np.empty((self.n, self.iters + 1), float)
        self.min_evaluations = np.empty((self.n, self.iters + 1), float)
        self.mean_evaluations = np.empty((self.n, self.iters + 1), float)

    def init(self):
        """Initialize starting values"""
        self.mean = np.zeros(self.individual_length)
        self.deviation = np.ones(self.individual_length)
        self.coefficients = self.random_coefficients()

    def random_coefficients(self) -> np.ndarray:
        """Generate coefficients with normal distribution"""
        def random_coefficient():
            coefficient = [np.random.normal(self.mean[i], self.deviation[i]) for i in range(self.individual_length)]
            return np.array(coefficient)
        return np.array([random_coefficient() for _ in range(self.population_size)])

    def model_estimation(self, coefficients):
        """Estimate probability parameters to generate better population"""
        pass

    def evaluate(self, i: int, x: int) -> np.ndarray:
        """Get and save new fitness values"""
        def evaluate_individual(idx, coefficient):
            return idx, np.sum(np.array(
                [Play(Game(), coefficient, self.objective_function, self.opponent_strategy).play() for _ in
                 range(self.population_size)]))

        values = np.zeros(self.population_size)
        results = Parallel(n_jobs=-1)(
            delayed(evaluate_individual)(idx, coefficient) for idx, coefficient in enumerate(self.coefficients))
        for idx, value in results:
            values[idx] = value
        self.max_evaluations[x][i] = np.max(values)
        self.min_evaluations[x][i] = np.min(values)
        self.mean_evaluations[x][i] = np.mean(values)
        return values

    def run(self, x) -> np.ndarray:
        """Single run of experiment"""
        pass

    def run_n_times(self) -> np.ndarray:
        """Save results from n runs of function"""
        for x in range(self.n):
            self.best_coefficients[x] = self.run(x)
        return self.best_coefficients

    def show_coefficients(self):
        """Show evaluation of results"""
        fig, axs = plt.subplots(3, 4, figsize=(12, 8))
        axs = axs.flatten()
        for i in range(self.best_coefficients.shape[1]):
            axs[i].plot(np.arange(self.best_coefficients.shape[0]), self.best_coefficients[:, i])
            axs[i].set_title(titles[i])
        plt.tight_layout()
        plt.show()

    def show(self):
        """Show evaluation of fitness function"""
        plt.figure()
        plt.title(self.__class__.__name__)
        plt.plot([self.population_size] * (self.iters + 1), color='r')
        plt.plot([-self.population_size] * (self.iters + 1), color='r')
        plt.plot(np.mean(self.max_evaluations, axis=0), label='max_evaluation')
        plt.plot(np.mean(self.min_evaluations, axis=0), label='min_evaluation')
        plt.plot(np.mean(self.mean_evaluations, axis=0), label='mean_evaluation')
        plt.legend()
        plt.show()
