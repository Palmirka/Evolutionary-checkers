from numpy import ndarray
from math import inf
from checkers_and_minimax_python_module import Engine, Color, Minimax, MoveList
from typing import Callable
from game.constants import MAX_POINTS
import random


class Play:
    def __init__(self, game: Engine, coefficients: ndarray, objective_function: Callable[[Engine, ndarray], float],
                    strategy: Callable[[Engine], MoveList]):
        self.game = game
        self.is_king = 0
        self.coefficients = coefficients
        self.objective_function = objective_function
        self.strategy = strategy
        self.minimax = Minimax()

    def find_best_move(self) -> MoveList:
        """Try *all* possible moves and pick best one"""
        moves = self.game.legal_moves_lists(self.game)
        best_move = {'field': None, 'value': -inf}
        for move in moves:
            old_game = Engine(self.game)
            old_game.act(move)
            value = self.objective_function(old_game, self.coefficients[:, self.is_king])
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

    # def points(self, player: Color) -> int:
    #     """Award points for game"""
    #     winner = self.game.isFinished()
    #     turn = self.game.move_turn
    #     # print(winner)
    #     if winner == player:
    #         return 100 - turn
    #     elif winner == 2:
    #         return 2
    #     elif winner >= 0:
    #         return turn - 100
    #     elif (self.game.black_kings() != 0 and player == Color.BLACK) or (self.game.white_kings() != 0 and player == Color.WHITE):
    #         return 100 - turn
    #     else:
    #         return turn - 100

    # def play(self, id, **strategy_args):
    #     """Gameplay against opponent"""
    #     self.game.reset()
    #     # print('Play thread: ', id)
    #     # player = random.choice([Color.WHITE, Color.BLACK])
    #     player = Color.WHITE
    #     while self.game.black_kings() + self.game.white_kings() == 0 and self.game.isFinished() < 0:
    #         while self.game.turn == Color.WHITE and self.game.black_kings() + self.game.white_kings() == 0 and self.game.isFinished() < 0:
    #             if self.game.turn == player:
    #                 self.game.act(self.find_best_move()['field'])
    #             else:
    #                 self.game.act(self.strategy(self.game, **strategy_args))
    #         while self.game.turn == Color.BLACK and self.game.black_kings() + self.game.white_kings() == 0 and self.game.isFinished() < 0:
    #             if self.game.turn == player:
    #                 self.game.act(self.find_best_move()['field'])
    #             else:
    #                 self.game.act(self.strategy(self.game, **strategy_args))
    #     return self.points(player)

    def play(self, id, **strategy_args):
        """Gameplay against opponent"""
        self.game.reset()
        player = Color.WHITE
        # player = random.choice([Color.WHITE, Color.BLACK])
        while self.game.isFinished() < 0:
            while self.game.turn == Color.WHITE and self.game.isFinished() < 0:
                if self.game.turn == player:
                    if self.game.white_kings() + self.game.black_kings() > 0:
                        print('Switch:', self.game.move_turn)
                        self.is_king = 1
                    self.game.act(self.find_best_move()['field'])
                else:
                    self.game.act(self.strategy(self.game, **strategy_args))
            while self.game.turn == Color.BLACK and self.game.isFinished() < 0:
                if self.game.turn == player:
                    if self.game.white_kings() + self.game.black_kings() > 0:
                        print('Switch:', self.game.turn)
                        self.is_king = 1
                    self.game.act(self.find_best_move()['field'])
                else:
                    self.game.act(self.strategy(self.game, **strategy_args))
        return self.points(player)
