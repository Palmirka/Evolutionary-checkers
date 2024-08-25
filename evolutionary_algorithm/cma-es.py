import cma
import numpy as np
from evolutionary_algorithm.base_functions.objective import Objective
from evolutionary_algorithm.evolutionary import Evolutionary
from move_strategies.strategies import MoveStrategy
from typing import Callable
from checkers_and_minimax_python_module import MoveList, Engine
from game.play import Play


def wrapped(params):
    total_score = 0
    num_games = 10  # Liczba gier do rozegrania w celu oceny strategii

    for _ in range(num_games):
        game_result = Play(self.pool[idx], pawns[idx], kings[idx], self.objective_function, self.opponent_strategy)
        total_score += game_result  # Zakładamy, że wygrana = +1, przegrana = -1, remis = 0

    # Możemy chcieć zmaksymalizować sumę punktów z gier
    return -total_score  # Negacja, ponieważ CMA-ES minimalizuje funkcję celu


class CMA_ES (Evolutionary):
    def __init__(self, objective: Objective, population_size: int, opponent_strategy: Callable[[MoveStrategy], MoveList],
                 iters: int, n: int,  **strategy_args):
        super().__init__(objective, population_size, 0, opponent_strategy, iters, n, **strategy_args)

    def run(self, x):
        self.init()
        values = self.evaluate(0, x)
        print(f'---------------------------------------------------')
        es = cma.CMAEvolutionStrategy(self.mean, 0.5)
        es.optimize(wrapped, iterations=20)
        best_solution = es.result.xbest
        print("Najlepsza strategia: ", best_solution)
        return self.coefficients_pawns[np.argmax(values)], self.coefficients_kings[np.argmax(values)]
