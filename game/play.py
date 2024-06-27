from game.constants import WHITE, BLACK
from numpy import ndarray
from math import inf
from copy import deepcopy
import random
from checkers.game import Game
from typing import Callable


class Play:
    def __init__(self, game: Game, coefficients: ndarray, objective_function: Callable[[Game, ndarray], float],
                 strategy):
        self.game = game
        self.coefficients = coefficients
        self.objective_function = objective_function
        self.strategy = strategy

    def find_best_move(self):
        """Try *all* possible moves and pick best one"""
        moves = self.game.get_possible_moves()
        best_move = {'field': None, 'value': -inf}
        for move in moves:
            old_game = deepcopy(self.game)
            old_game.move(move)
            value = self.objective_function(old_game, self.coefficients)
            if value > best_move['value']:
                best_move = {'field': move, 'value': value}
        return best_move

    def points(self):
        """Award points for game"""
        winner = self.game.get_winner()
        if winner is None:
            return 0
        elif winner == 1:
            return 1
        else:
            return -1

    def play(self):
        """Gameplay against opponent"""
        self.game.board.player_turn = random.choice([WHITE, BLACK])
        while not self.game.is_over():
            if self.game.whose_turn() == WHITE:
                best_move = self.find_best_move()
                self.game.move(best_move['field'])
            else:
                self.game.move(self.strategy(self.game))
        return self.points()
