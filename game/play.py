from numpy import ndarray
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
            # old_game.print()
            value = self.objective_function(old_game, coefficients, self.diff, self.is_king)
            # print('     Move:', value)
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
    #         return MAX_POINTS - turn
    #     elif winner == 2:
    #         return 0
    #     elif winner >= 0:
    #         return turn - MAX_POINTS
    #     elif (self.game.black_kings() != 0 and player == Color.BLACK) or (self.game.white_kings() != 0 and player == Color.WHITE):
    #         return MAX_POINTS - turn
    #     else:
    #         return turn - MAX_POINTS

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
                        self.is_king = 1
                    self.game.act(self.find_best_move()['field'])
                else:
                    self.game.act(self.strategy(self.game, **strategy_args))
            if self.game.turn == Color.BLACK and self.game.isFinished() < 0:
                if self.game.turn == player:
                    if self.game.white_kings() + self.game.black_kings() > 0:
                        self.is_king = 1
                    self.game.act(self.find_best_move()['field'])
                else:
                    self.game.act(self.strategy(self.game, **strategy_args))
        return self.points(player)
