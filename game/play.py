from numpy import ndarray
import numpy as np
from math import inf
from checkers_and_minimax_python_module import Engine, Color, Minimax, MoveList
from typing import Callable
from game.constants import MAX_POINTS


class Play:
    def __init__(self, game: Engine, coefficients_pawns: ndarray, coefficients_kings: ndarray, diff: float,
                 objective_function: Callable[[Engine, ndarray, float, bool], float], strategy: Callable[[Engine], MoveList]):
        self.game = game
        self.is_king = False
        self.coefficients_pawns = coefficients_pawns
        self.coefficients_kings = coefficients_kings
        self.diff = diff
        self.objective_function = objective_function
        self.strategy = strategy
        self.minimax = Minimax()

    def find_best_move(self) -> MoveList:
        """Try *all* possible moves and pick best one"""
        moves = self.game.legal_moves_lists(self.game)
        best_move = {'field': None, 'value': -inf}
        coefficients = self.coefficients_kings if self.is_king else self.coefficients_pawns
        for move in moves:
            old_game = Engine(self.game)
            old_game.act(move)
            value = self.objective_function(old_game, coefficients, self.diff, self.is_king)
            if value > best_move['value']:
                best_move = {'field': move, 'value': value}
        return best_move

    def points(self, player: Color) -> int:
        """Award points for game"""
        winner = self.game.isFinished()
        turn = self.game.move_turn
        if winner == player:
            return MAX_POINTS - turn
        elif winner == 2:
            return 0
        return turn - MAX_POINTS

    def play(self, idx, n):
        """Gameplay against opponent"""
        def single_gameplay():
            self.game.reset()
            player = Color.WHITE
            # player = random.choice([Color.WHITE, Color.BLACK])
            while self.game.isFinished() < 0:
                while self.game.turn == Color.WHITE and self.game.isFinished() < 0:
                    if self.game.turn == player:
                        if self.game.white_kings() + self.game.black_kings() > 0:
                            self.is_king = 1
                        self.game.act(self.find_best_move()['field'])
                    else:
                        self.game.act(self.strategy(self.game))
                if self.game.turn == Color.BLACK and self.game.isFinished() < 0:
                    if self.game.turn == player:
                        if self.game.white_kings() + self.game.black_kings() > 0:
                            self.is_king = 1
                        self.game.act(self.find_best_move()['field'])
                    else:
                        self.game.act(self.strategy(self.game))
            return self.points(player)

        return np.mean(np.array([single_gameplay() for _ in range(n)]))
