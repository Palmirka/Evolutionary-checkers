import random
from checkers_and_minimax_python_module import Engine, Minimax, Color


class MoveStrategy:
    """Tested strategies against our AI"""

    @staticmethod
    def first_in_row(game: Engine, **kwargs):
        """Take first found move"""
        return game.legal_moves_lists(game)[0]

    @staticmethod
    def random(game: Engine, **kwargs):
        """Take random move"""
        moves = game.legal_moves_lists(game)
        return moves[random.randint(0, len(moves) - 1)]

    @staticmethod
    def minimax(game: Engine, **kwargs):
        minimax = Minimax()
        print(kwargs)
        return minimax.minimax_move(game, kwargs.get('depth', 2), Color.BLACK)
