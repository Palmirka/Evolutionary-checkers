from checkers.game import Game
from joblib import Parallel, delayed
from numpy import inf
from copy import deepcopy
from typing import Callable, Tuple


def alpha_beta_minimax(max_depth: int) -> Callable[[Game], Tuple[int, int]]:
    def evaluate(game: Game):
        return len(game.board.searcher.player_pieces[2]) - len(game.board.searcher.player_pieces[1])

    def recurse(game, depth, alpha, beta, maximum):
        if depth <= 0 or game.is_over():
            return {'field': None, 'value': evaluate(game)}

        if maximum:
            moves = game.get_possible_moves()
            best_move = {'field': None, 'value': -inf}
            results = Parallel(n_jobs=-1)(
                delayed(evaluate_move)(deepcopy(game), move, depth - 1, False) for move in moves
            )
            for result in results:
                if result['value'] > best_move['value']:
                    best_move = result
            return best_move

        else:
            moves = game.get_possible_moves()
            best_move = {'field': None, 'value': inf}
            results = Parallel(n_jobs=-1)(
                delayed(evaluate_move)(deepcopy(game), move, depth - 1, True) for move in moves
            )
            for result in results:
                if result['value'] < best_move['value']:
                    best_move = result
            return best_move

    def evaluate_move(game, move, depth, maximum):
        game.move(move)
        result = recurse(game, depth, maximum)
        result['field'] = move
        return result

    def minimax_helper(game: Game) -> (int, int):
        best_move = recurse(game, max_depth, True)
        return best_move['field']

    return minimax_helper
