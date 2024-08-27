import random
from checkers_and_minimax_python_module import Engine, Minimax, Color


class MoveStrategy:
    """Tested strategies against our AI"""

    def __init__(self, **strategy_kwargs):
        self.strategy_kwargs = strategy_kwargs

    def first_in_row(self, game: Engine):
        """Take first found move"""
        return game.legal_moves_lists(game)[0]

    def random(self, game: Engine):
        """Take random move"""
        moves = game.legal_moves_lists(game)
        return moves[random.randint(0, len(moves) - 1)]

    def minimax(self, game: Engine):
        minimax = Minimax()
        return minimax.minimax_move(game, self.strategy_kwargs.get('depth', 2), Color.BLACK)
