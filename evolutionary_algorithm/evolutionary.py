import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
from joblib import Parallel, delayed
import multiprocessing as mp
from checkers_and_minimax_python_module import Engine, MoveList
from move_strategies.strategies import MoveStrategy
from game.play import Play
from game.constants import MAX_POINTS
from typing import Callable, Dict
import time


# def evaluate_individual(args):
#     idx, coefficient, engine, objective_function, opponent_strategy, population_size = args
#     play_instance = Play(engine, coefficient, objective_function, opponent_strategy)
#     return idx, np.mean([play_instance.play() for _ in range(population_size)])

class Evolutionary:
    def __init__(self, objective, population_size: int, descendant_size: int,
                 opponent_strategy: Callable[[MoveStrategy], MoveList], iters: int, n: int, **strategy_args):
        """Initialize evolutionary and diagram parameters"""
        self.pool = np.array([Engine() for _ in range(population_size)])
        # self.engine = Engine()
        self.mean = None
        self.deviation = None
        self.opponent_strategy = opponent_strategy
        self.strategy_args = strategy_args
        self.objective_function = objective.function
        self.coefficients = np.empty((population_size, objective.size), float)
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
        # start_time = time.time()
        """Get and save new fitness values"""

        def evaluate_individual(idx, coefficients):
            return idx, Play(self.pool[idx], coefficients, self.objective_function, self.opponent_strategy).play(idx, **self.strategy_args)


        # values = np.zeros(self.population_size)
        #
        # # Create a Queue to collect results
        # result_queue = mp.Queue()
        # processes = []
        #
        # # Start processes
        # for idx, coefficient in enumerate(self.coefficients):
        #     mp.set_start_method('fork')
        #     p = mp.Process(target=evaluate_individual, args=(idx, coefficient, result_queue))
        #     p.start()
        #     processes.append(p)
        #
        # # Wait for all processes to finish
        # for p in processes:
        #     p.join()
        #
        # # Collect results
        values = np.zeros(self.population_size)
        # while not result_queue.empty():
        #     idx, value = result_queue.get()
        #     values[idx] = value

        for idx, coefficient in enumerate(self.coefficients):
            _, values[idx] = evaluate_individual(idx, coefficient)

        # with ThreadPoolExecutor(max_workers=self.population_size) as executor:
        #     futures = [executor.submit(evaluate_individual, idx, coefficient)
        #                for idx, coefficient in enumerate(self.coefficients)]
        #
        #     for future in as_completed(futures):
        #         idx, value = future.result()
        #         values[idx] = value

        # results = Parallel(n_jobs=-1, backend='threading')(
        #     delayed(evaluate_individual)(idx, coefficient) for idx, coefficient in enumerate(self.coefficients))
        # for idx, value in results:
        #     values[idx] = value

        self.max_evaluations[x][i] = np.max(values)
        self.min_evaluations[x][i] = np.min(values)
        self.mean_evaluations[x][i] = np.mean(values)
        # end_time = time.time()
        # print('Evaluate time: ', end_time - start_time)
        return values

    def run(self, x) -> np.ndarray:
        """Single run of experiment"""
        pass

    def run_n_times(self) -> np.ndarray:
        """Save results from n runs of function"""

        # with ProcessPoolExecutor(max_workers=self.n) as executor:
        #     futures = [executor.submit(lambda x=x: (x, self.run(x))) for x in range(self.n)]
        #
        #     for future in as_completed(futures):
        #         x, result = future.result()
        #         self.best_coefficients[x] = result

        # def worker(x):
        #     """Worker function for multiprocessing"""
        #     return self.run(x)
        #
        # mp.set_start_method('fork', force=True)
        # with mp.Pool(processes=self.n) as pool:
        #     results = pool.map(worker, range(self.n))
        #
        # self.best_coefficients = np.array(results)

        for x in range(self.n):
            self.best_coefficients[x] = self.run(x)

        return self.best_coefficients

    def show(self):
        """Show evaluation of fitness function"""
        plt.figure()
        plt.title(self.__class__.__name__)
        plt.plot([MAX_POINTS] * (self.iters + 1), color='r')
        plt.plot([- MAX_POINTS] * (self.iters + 1), color='r')
        plt.plot(np.mean(self.max_evaluations, axis=0), label='max_evaluation')
        plt.plot(np.mean(self.min_evaluations, axis=0), label='min_evaluation')
        plt.plot(np.mean(self.mean_evaluations, axis=0), label='mean_evaluation')
        plt.legend()
        plt.show()



