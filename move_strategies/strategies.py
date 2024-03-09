import random
from typing import Tuple
from checkers.game import Game
from move_strategies.minimax import alpha_beta_minimax


class MoveStrategy:
    """Tested strategies against our AI"""

    def __init__(self, game: Game):
        """Initialize move parameters"""
        self.game = game

    def first_in_row(self) -> Tuple[int, int]:
        """Take first found move"""
        return self.game.get_possible_moves()[0]

    def random(self) -> Tuple[int, int]:
        """Take random move"""
        moves = self.game.get_possible_moves()
        return moves[random.randint(0, len(moves) - 1)]

    def minimax(self, depth: int) -> Tuple[int, int]:
        """Recursively look for best move to given depth"""
        minimax = alpha_beta_minimax(depth)
        return minimax(self.game)
