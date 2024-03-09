import numpy as np
from checkers.game import Game


class Objective:
    @staticmethod
    def function(game: Game, coefficients: np.ndarray) -> float:
        """Fitness function that grades actual board state"""
        # based on https://pages.mini.pw.edu.pl/~mandziukj/PRACE/es_init.pdf
        board = game.board

        def check(position, king=None, player=1):
            piece = board.searcher.get_piece_by_position(position)
            if piece:
                return (king is None or piece.king == king) and piece.player == player
            return False

        def check_multiple(positions, king=None, player=1):
            return np.array([check(position, king, player) for position in positions])

        data_vector = np.ones(12, dtype=int)
        # 0 - pawns
        data_vector[0] = len(list(filter(lambda x: not x.king, board.searcher.player_pieces[1])))
        # 1 - kings
        data_vector[1] = len(board.searcher.player_pieces[1]) - data_vector[0]
        # 2 - safe pawns
        edges = [1, 2, 3, 4, 12, 20, 28, 32, 31, 30, 29, 21, 13, 5]
        data_vector[2] = np.sum(check_multiple(edges))
        # 3 - attacking pawns
        data_vector[3] = len(set(map(lambda x: x[0], board.get_possible_capture_moves())))
        # 4 - centrally positioned pawns
        central = np.array([10, 11, 14, 15, 18, 19, 22, 23])
        data_vector[4] = np.sum(check_multiple(central, False))
        # 5 - centrally positioned kings
        data_vector[5] = np.sum(check_multiple(central, True))
        # 6 - king on double diagonal
        double_diagonal = np.array([1, 5, 6, 9, 10, 14, 15, 18, 19, 23, 24, 27, 28, 32])
        data_vector[5] = np.sum(check_multiple(double_diagonal, True))
        # 7 - bridge patterns
        data_vector[9] = int(check(1) and check(3))
        # 8 - oreo patterns
        data_vector[8] = int(check(2) and check(3) and check(7))
        # 9 - triangle patterns
        data_vector[9] = int(check(1) and check(2) and check(6))
        # 10 - dog patterns
        data_vector[10] = int(check(1) and check(5, player=2))
        # 11 - king in corner patterns
        data_vector[11] = int(check(29, True))
        # print(data_vector)
        values = coefficients * data_vector
        return values.sum()
