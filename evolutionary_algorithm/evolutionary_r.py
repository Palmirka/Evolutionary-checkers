import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
from game.play import Play
from game.constants import MAX_POINTS
from typing import Callable


class Evolutionary:
    def __init__(self, objective, population_size: int, descendant_size: int,
                 opponent_strategy: Callable[[MoveStrategy], MoveList], iters: int, n: int, **strategy_args):
        """Initialize evolutionary and diagram parameters"""
        self.pool = np.array([[Engine() for _ in range(population_size)] for _ in range(n)])
        self.mean = None
        self.deviation = None
        self.opponent_strategy = opponent_strategy
        self.strategy_args = strategy_args
        self.objective_function = objective.function
        self.coefficients = np.empty((n, population_size, objective.size), float)
        self.population_size = population_size
        self.descendant_size = descendant_size
        self.individual_length = objective.size
        self.iters = iters
        self.n = n

        self.best_coefficients = np.empty((self.n, self.individual_length))
        self.max_evaluations = np.empty((self.n, self.iters + 1), float)
        self.min_evaluations = np.empty((self.n, self.iters + 1), float)
        self.mean_evaluations = np.empty((self.n, self.iters + 1), float)

    def init(self):
        """Initialize starting values"""
        self.mean = np.array([np.zeros(self.individual_length) for _ in range(self.n)])
        self.deviation = np.array([np.ones(self.individual_length) for _ in range(self.n)])
        self.coefficients = np.array([self.random_coefficients(x) for x in range(self.n)])

    def random_coefficients(self, x) -> np.ndarray:
        """Generate coefficients with normal distribution"""

        def random_coefficient():
            coefficient = [np.random.normal(self.mean[x][i], self.deviation[x][i]) for i in range(self.individual_length)]
            return np.array(coefficient)

        return np.array([random_coefficient() for _ in range(self.population_size)])

    def model_estimation(self, coefficients, x):
        """Estimate probability parameters to generate better population"""
        pass

    def evaluate(self, i: int, x: int) -> np.ndarray:
        """Get and save new fitness values"""

        def evaluate_individual(idx, coefficients):
            self.pool[x][idx].reset()
            return idx, Play(self.pool[x][idx], coefficients, self.objective_function, self.opponent_strategy).play(idx, **self.strategy_args)

        values = np.zeros(self.population_size)

        # for idx, coefficient in enumerate(self.coefficients):
        #     _, values[idx] = evaluate_individual(idx, coefficient)

        results = Parallel(n_jobs=-1)(
            delayed(evaluate_individual)(idx, coefficient) for idx, coefficient in enumerate(self.coefficients[x]))

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

        # results = Parallel(n_jobs=-1)(
        #     delayed(self.run)(x) for x in range(self.n))

        for x in range(self.n):
            self.best_coefficients[x] = self.run(x)

        return self.best_coefficients

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



