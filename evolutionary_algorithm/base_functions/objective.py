import numpy as np
from evolutionary_algorithm.preparation.combination_check import check_board
from evolutionary_algorithm.preparation.masking import binary_of_keys
from evolutionary_algorithm.preparation.reader import read_file
from checkers_and_minimax_python_module import Engine


class Objective:
    def __init__(self):
        self.dict = read_file("boards_analyse_2x2_32897_games.txt", 0)[0]
        self.dict.update(read_file("boards_analyse_3x3_32897_games.txt", 2048)[0])
        self.dict.update(read_file("boards_analyse_4x4_32897_games.txt", 4096)[0])
        self.size, self.usage, self.values_white, self.values_black, self.values_w_king, self.values_b_king = binary_of_keys(self.dict)
        print(self.size)

    def function(self, game: Engine, coefficients: np.ndarray) -> float:
        """Fitness function that grades actual board state"""

        masks = bin(check_board(game.white_pieces(), game.black_pieces(), game.white_kings(), game.black_kings(),
                                self.usage, self.values_white, self.values_black, self.values_w_king, self.values_b_king,
                                self.size))[2:].zfill(self.size)
        result = sum([c if masks[idx] == '1' else 0 for idx, c in enumerate(coefficients)])
        # result = bin(game.white_pieces()).count('1') - bin(game.black_pieces()).count('1')
        return result
